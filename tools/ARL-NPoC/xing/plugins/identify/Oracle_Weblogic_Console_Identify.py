from xing.core.BasePlugin import BasePlugin
from xing.utils import http_req, get_logger
from xing.core import PluginType, SchemeType


class Plugin(BasePlugin):
    def __init__(self):
        super(Plugin, self).__init__()
        self.plugin_type = PluginType.POC
        self.vul_name = "发现 Oracle Weblogic 控制台"
        self.app_name = 'weblogic'
        self.scheme = [SchemeType.HTTP, SchemeType.HTTPS]

    def verify(self, target):
        path_list = ["/#/console/css/test.css", "/#/../console/css/test.css", "/#/../../console/css/test.css",
                     "/console/css/test.css;/../../../"]

        check = b"WLS Administration Console"
        for path in path_list:
            url = target + path
            conn = http_req(url, disable_normal=True)
            if check in conn.content:
                self.logger.success("found {} {}".format(self.app_name, url))
                return url
