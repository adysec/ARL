from xing.core.BasePlugin import BasePlugin
from xing.utils import http_req
from xing.core import PluginType, SchemeType


class Plugin(BasePlugin):
    def __init__(self):
        super(Plugin, self).__init__()
        self.plugin_type = PluginType.POC
        self.vul_name = "Apache solr 未授权访问"
        self.app_name = 'solr'
        self.scheme = [SchemeType.HTTPS, SchemeType.HTTP]

    def verify(self, target):
        paths = ["/solr/admin/cores?wt=json&indexInfo=false", "/admin/cores?wt=json&indexInfo=false"]
        for path in paths:
            url = target + path
            conn = http_req(url)
            if b"<" in conn.content:
                continue

            if b"responseHeader" in conn.content:
                self.logger.success("发现 Apache solr 未授权访问 {}".format(url))
                return url
