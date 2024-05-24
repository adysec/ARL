from xing.core.BasePlugin import BasePlugin
from xing.utils import http_req
from xing.core import PluginType, SchemeType


class Plugin(BasePlugin):
    def __init__(self):
        super(Plugin, self).__init__()
        self.plugin_type = PluginType.POC
        self.vul_name = "发现 Grafana"
        self.app_name = 'Grafana'
        self.scheme = [SchemeType.HTTP, SchemeType.HTTPS]

    def verify(self, target):
        path_list = ["/login", "/grafana/login", "/monitor/login"]
        check = b"Grafana</title>"
        for path in path_list:
            url = target + path
            conn = http_req(url)
            if check in conn.content:
                self.logger.success("found {} {}".format(self.app_name, url))
                return url
