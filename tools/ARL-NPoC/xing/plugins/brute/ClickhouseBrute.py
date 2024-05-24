from xing.core.BasePlugin import BasePlugin
from xing.utils import http_req
from xing.core import PluginType, SchemeType


class Plugin(BasePlugin):
    def __init__(self):
        super(Plugin, self).__init__()
        self.plugin_type = PluginType.BRUTE
        self.vul_name = "Clickhouse 弱口令"
        self.app_name = 'Clickhouse'
        self.scheme = [SchemeType.HTTP, SchemeType.HTTPS]

        self._check_str = b'Authentication failed'
        self.username_file = "username_clickhouse.txt"
        self.password_file = "password_clickhouse.txt"
        self.shuffle_auth_list = True

    def login(self, target, user, passwd):
        url = target + "/"
        headers = {
            "X-ClickHouse-User": user,
            "X-ClickHouse-Key": passwd
        }
        conn = http_req(url, "post", data="", headers=headers)
        if b'(SYNTAX_ERROR)' not in conn.content:
            return False

        if conn.status_code != 400:
            return False

        return True

    def check_app(self, target):
        url = target + "/"
        headers = {
            "X-ClickHouse-User": "xxxx1",
            "X-ClickHouse-Key": "notkey"
        }
        conn = http_req(url, "post", data="", headers=headers)

        if self._check_str not in conn.content:
            return False

        if b'<title' in conn.content:
            return False

        if conn.status_code == 403:
            return True
        else:
            return False
