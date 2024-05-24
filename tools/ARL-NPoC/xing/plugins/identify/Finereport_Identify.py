from xing.core.BasePlugin import BasePlugin
from xing.utils import http_req, get_logger
from xing.core import PluginType, SchemeType


class Plugin(BasePlugin):
    def __init__(self):
        super(Plugin, self).__init__()
        self.plugin_type = PluginType.POC
        self.vul_name = "发现帆软 FineReport"
        self.app_name = 'FineReport'
        self.scheme = [SchemeType.HTTP, SchemeType.HTTPS]

    def verify(self, target):
        path_list = ["/webroot/", "/WebReport/", "/seeyonreport/"]
        check_path = "ReportServer?op=resource&resource=/com/fr/web/jquery.js"
        check = b"jQuery="

        for path in path_list:
            url = target + path + check_path
            conn = http_req(url)

            if check in conn.content and b"<title>" not in conn.content:
                self.logger.success("found FineReport {}".format(url))
                return target + path + "ReportServer"

