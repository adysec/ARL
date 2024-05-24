from xing.core.BasePlugin import BasePlugin
from xing.utils import http_req, get_logger
from xing.core import PluginType, SchemeType


class Plugin(BasePlugin):
    def __init__(self):
        super(Plugin, self).__init__()
        self.plugin_type = PluginType.POC
        self.vul_name = "发现帆软 FineReport V10"
        self.app_name = 'FineReport'
        self.scheme = [SchemeType.HTTP, SchemeType.HTTPS]

    def verify(self, target):
        path_list = ["/webroot/decision/system/info", "/decision/system/info"]

        for path in path_list:
            url = target + path
            conn = http_req(url)

            if b"frontSeed" in conn.content and b'name' in conn.content:
                self.logger.success("found FineReport V10 {}".format(url))
                return url

