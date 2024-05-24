from xing.core.BasePlugin import BasePlugin
from xing.utils import http_req
from xing.core import PluginType, SchemeType


class Plugin(BasePlugin):
    def __init__(self):
        super(Plugin, self).__init__()
        self.plugin_type = PluginType.BRUTE
        self.vul_name = "Tomcat 弱口令"
        self.app_name = 'Tomcat'
        self.scheme = [SchemeType.HTTP, SchemeType.HTTPS]

        self._check_str = 'Tomcat'
        self.username_file = "username_tomcat.txt"
        self.password_file = "password_tomcat.txt"
        self.shuffle_auth_list = True

    def login(self, target, user, passwd):
        url = target + "/manager/html"
        conn = http_req(url, "get", auth=(user, passwd))
        if conn.status_code == 200:
            return True

    def check_app(self, target):
        url = target + "/manager/html"
        conn = http_req(url, "get")

        if self._check_str not in conn.headers.get("WWW-Authenticate", ""):
            return False

        if conn.status_code == 401:
            return True
        else:
            return False
