import base64
from xing.core.BasePlugin import BasePlugin
from xing.utils import http_req, get_logger
from xing.core import PluginType, SchemeType


class Plugin(BasePlugin):
    def __init__(self):
        super(Plugin, self).__init__()
        self.plugin_type = PluginType.BRUTE
        self.vul_name = "Jenkins 弱口令"
        self.app_name = 'Jenkins'
        self.scheme = [SchemeType.HTTP, SchemeType.HTTPS]

        self._check_str = b'Authentication required'
        self.username_file = "username_jenkins.txt"
        self.password_file = "password_jenkins.txt"

    def login(self, target, user, passwd):
        url = target + "/api/json"
        auth = base64.b64encode("{}:{}".format(user, passwd).encode()).decode()
        headers = {
            "Authorization": "Basic {}".format(auth)
        }
        conn = http_req(url, "get", headers=headers)
        if b'jenkins' not in conn.content:
            return False

        if conn.status_code != 200:
            return False

        if conn.json():
            return True

    def check_app(self, target):
        url = target + "/api/json"
        conn = http_req(url, "get")

        if self._check_str not in conn.content:
            return False

        if b'<title' in conn.content:
            return False

        if conn.status_code == 403:
            return True
        else:
            return False
