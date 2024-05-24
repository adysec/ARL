import base64
from xing.core.BasePlugin import BasePlugin
from xing.utils import http_req, random_choices
from xing.core import PluginType, SchemeType


class Plugin(BasePlugin):
    def __init__(self):
        super(Plugin, self).__init__()
        self.plugin_type = PluginType.BRUTE
        self.vul_name = "Openfire 弱口令"
        self.app_name = 'Openfire'
        self.scheme = [SchemeType.HTTP, SchemeType.HTTPS]

        self._check_str = b'Openfire'
        self.username_file = "username_openfire.txt"
        self.password_file = "password_openfire.txt"
        self.shuffle_auth_list = True

    def login(self, target, user, passwd):

        # 15分钟内，只能尝试10次
        url = target + "/login.jsp"
        csrf = random_choices(10)
        location_url = random_choices(6) + ".jsp"
        headers = {
            "Cookie": "csrf={}".format(csrf)
        }
        data = {
            "url": "/{}".format(location_url),
            "login": "true",
            "csrf": csrf,
            "username": user,
            "password": passwd
        }

        conn = http_req(url, "post", headers=headers,  data=data)
        location = conn.headers.get("Location", "")

        if location_url not in location:
            return False

        if conn.status_code == 301 or conn.status_code == 302:
            return True

    def check_app(self, target):
        url = target + "/login.jsp"
        conn = http_req(url, "get")

        if self._check_str not in conn.content:
            return False

        if conn.status_code == 200:
            return True
        else:
            return False
