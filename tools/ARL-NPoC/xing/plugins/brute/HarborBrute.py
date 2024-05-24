import time
from base64 import b64encode
from xing.core.BasePlugin import BasePlugin
from xing.utils import http_req
from xing.core import PluginType, SchemeType


class Plugin(BasePlugin):
    def __init__(self):
        super(Plugin, self).__init__()
        self.plugin_type = PluginType.BRUTE
        self.vul_name = "Harbor 弱口令"
        self.app_name = 'Harbor'
        self.scheme = [SchemeType.HTTP, SchemeType.HTTPS]

        self.login_path = "/api/users"
        self.username_file = "username_harbor.txt"
        self.password_file = "password_harbor.txt"

    def login(self, target, user, passwd):
        auth = b64encode("{}:{}".format(user, passwd).encode()).decode()
        headers = {
            "Content-Type": "application/json",
            "Authorization": "Basic {}".format(auth),
        }
        url = target + self.login_path
        req = http_req(url, "get", headers=headers)
        if b'<' in req.content:
            return False
        if req.status_code == 200:
            return True

    def check_app(self, target):
        url = target + self.login_path
        headers = {
            "Content-Type": "application/json",
            "Authorization": "asic MTox",
        }
        req = http_req(url, "get", headers=headers)
        if req.status_code == 401:
            return True
