import base64
from xing.core.BasePlugin import BasePlugin
from xing.utils import http_req, get_logger
from xing.core import PluginType, SchemeType


class Plugin(BasePlugin):
    def __init__(self):
        super(Plugin, self).__init__()
        self.plugin_type = PluginType.BRUTE
        self.vul_name = "Grafana 弱口令"
        self.app_name = 'Grafana'
        self.scheme = [SchemeType.HTTP, SchemeType.HTTPS]

        self._check_str = b'Invalid username or password'
        self.username_file = "username_grafana.txt"
        self.password_file = "password_grafana.txt"
        self.shuffle_auth_list = True

    def login(self, target, user, passwd):
        """
        Grafana 登录爆破，不过存在防爆破。
        """
        url = target + "/login"
        data = {
            "user": user,
            "password": passwd
        }
        conn = http_req(url, "post", json=data)
        if b'Logged in' not in conn.content:
            return False

        if conn.status_code != 200:
            return False

        if conn.json():
            return True

    def check_app(self, target):
        url = target + "/login"
        data = {
            "user": "jla1j23",
            "password": "jla1j23"
        }
        conn = http_req(url, "post", json=data)

        if self._check_str not in conn.content:
            return False

        if b'<title' in conn.content:
            return False

        if conn.status_code == 401:
            return True
        else:
            return False
