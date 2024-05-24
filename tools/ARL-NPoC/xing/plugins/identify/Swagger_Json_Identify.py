from xing.core.BasePlugin import BasePlugin
from xing.utils import http_req, get_logger
from xing.core import PluginType, SchemeType


class Plugin(BasePlugin):
    def __init__(self):
        super(Plugin, self).__init__()
        self.plugin_type = PluginType.POC
        self.vul_name = "发现 Swagger 文档接口"
        self.app_name = 'Swagger'
        self.scheme = [SchemeType.HTTP, SchemeType.HTTPS]

    def verify(self, target):
        paths = ["/swagger.json", "/api/swagger.json", "/swagger/v1/swagger.json", "/v2/api-docs"]
        paths += ["/api/v2/api-docs", "/api/v2/swagger.json"]

        for path in paths:
            url = target + path
            conn = http_req(url)
            if conn.status_code != 200:
                continue
            text = conn.text.strip()
            if not text.startswith("{"):
                continue

            if not text.endswith("}"):
                continue

            check_str = ['"paths"', '"swagger"']

            if check_str[0] not in text:
                continue

            if check_str[1] not in text:
                continue
            self.logger.success("Found swagger url {}".format(url))
            return url
