from xing.core.BasePlugin import BasePlugin
from xing.utils import http_req
from xing.core import PluginType, SchemeType


class Plugin(BasePlugin):
    def __init__(self):
        super(Plugin, self).__init__()
        self.plugin_type = PluginType.POC
        self.vul_name = "Onlyoffice 未授权漏洞"
        self.app_name = 'Onlyoffice'
        self.scheme = [SchemeType.HTTP, SchemeType.HTTPS]

    def verify(self, target):
        paths = ["/ConvertService.ashx"]
        for path in paths:
            url = target + path
            conn = http_req(url)
            if b'<Error>-7</Error>' in conn.content and b'<?xml' in conn.content:
                self.logger.success("found Onlyoffice {}".format(url))
                return True
