from xing.core.BasePlugin import BasePlugin
from xing.utils import http_req
from xing.core import PluginType, SchemeType


class Plugin(BasePlugin):
    def __init__(self):
        super(Plugin, self).__init__()
        self.plugin_type = PluginType.POC
        self.vul_name = "Druid 未授权访问"
        self.app_name = 'Druid'
        self.scheme = [SchemeType.HTTPS, SchemeType.HTTP]

    def verify(self, target):
        url = target + "/druid/webapp.json"
        conn = http_req(url)
        if b'<' in conn.content:
            return False

        if b'"ResultCode"' not in conn.content:
            return False

        if b'"RequestCount"' in conn.content:
            self.logger.success("发现 Druid 未授权访问 {}".format(self.target))
            return url
