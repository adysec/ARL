from xing.core.BasePlugin import BasePlugin
from xing.utils import http_req
from xing.core import PluginType, SchemeType


class Plugin(BasePlugin):
    def __init__(self):
        super(Plugin, self).__init__()
        self.plugin_type = PluginType.POC
        self.vul_name = "Elasticsearch 未授权访问"
        self.app_name = 'Elasticsearch'
        self.scheme = [SchemeType.HTTPS, SchemeType.HTTP]

    def verify(self, target):
        url = target + "/_cat"
        conn = http_req(url)
        if b'/_cat/master' in conn.content and b"<" not in conn.content:
            self.logger.success("发现 Elasticsearch 未授权访问 {}".format(self.target))
            return True
