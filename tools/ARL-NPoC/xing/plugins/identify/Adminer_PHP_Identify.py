from xing.core.BasePlugin import BasePlugin
from xing.utils import http_req, get_logger
from xing.core import PluginType, SchemeType


class Plugin(BasePlugin):
    def __init__(self):
        super(Plugin, self).__init__()
        self.plugin_type = PluginType.POC
        self.vul_name = "发现 Adminer.php"
        self.app_name = 'Adminer.php'
        self.scheme = [SchemeType.HTTP, SchemeType.HTTPS]

    def verify(self, target):
        path_list = ["/admin/", "/", "/adminer/"]
        check_path = "adminer.php"
        check = b">Login - Adminer<"

        for path in path_list:
            url = target + path + check_path
            headers = {
                "Accept-Language": "en"
            }
            conn = http_req(url, headers=headers)

            if check in conn.content:
                self.logger.success("found Adminer.php {}".format(url))
                return url

