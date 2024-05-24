import json
from xing.core.BasePlugin import BasePlugin
from xing.utils import http_req
from xing.core import PluginType, SchemeType


class Plugin(BasePlugin):
    def __init__(self):
        super(Plugin, self).__init__()
        self.plugin_type = PluginType.BRUTE
        self.vul_name = "APISIX 弱口令"
        self.app_name = 'APISIX'
        self.scheme = [SchemeType.HTTP, SchemeType.HTTPS]

        self.username_file = "username_apisix.txt"
        self.password_file = "password_apisix.txt"
        self.shuffle_auth_list = True


    def login(self, target, user, passwd):
        url = target + "/apisix/admin/user/login"
        login = {
            "username": user,
            "password": passwd
        }
        
        req = http_req(url, "post", json=login)

        if b'"code":0' in req.content:
            if b'"token"' in req.content:
                return True

    def check_app(self, target):
        url = target + "/apisix/admin/user/login"
        check = {
            "test": 1
        }
        
        req = http_req(url, "post", json=check)

        if b'"code":10004' not in req.content:
            return False
            
        if req.status_code == 200:
            return True
