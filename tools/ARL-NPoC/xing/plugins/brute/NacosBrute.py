from xing.core.BasePlugin import BasePlugin
from xing.utils import http_req
from xing.core import PluginType, SchemeType


class Plugin(BasePlugin):
    def __init__(self):
        super(Plugin, self).__init__()
        self.plugin_type = PluginType.BRUTE
        self.vul_name = "Nacos 弱口令"
        self.app_name = 'Nacos'
        self.scheme = [SchemeType.HTTP, SchemeType.HTTPS]

        self.username_file = "username_nacos.txt"
        self.password_file = "password_nacos.txt"
        self.shuffle_auth_list = True

    def login(self, target, user, passwd):
        url = target + "/nacos/v1/auth/users/login"
        data = {
            "username": user,
            "password": passwd
        }
        conn = http_req(url, "post", data=data)
        if conn.status_code != 200:
            return False

        if b"<" in conn.content:
            return False

        if b'"accessToken":"e' in conn.content:
            return True

    def check_app(self, target):
        url = target + "/nacos/"
        conn = http_req(url, "get")

        if b'<title>Nacos</title>' not in conn.content:
            return False

        return True
