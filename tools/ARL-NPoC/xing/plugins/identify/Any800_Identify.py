from xing.core.BasePlugin import BasePlugin
from xing.utils import http_req, get_logger
from xing.core import PluginType, SchemeType


# 官方演示站点 http://www.any800.com/


class Plugin(BasePlugin):
    def __init__(self):
        super(Plugin, self).__init__()
        self.plugin_type = PluginType.POC
        self.vul_name = "发现 Any800全渠道智能客服云平台"
        self.app_name = 'Any800'
        self.scheme = [SchemeType.HTTP, SchemeType.HTTPS]

    def verify(self, target):
        check_map = {
            "/any800/echatManager.do": b"new Date(nowtime_time+offset+offset_b);",
            "/ump/umpLogin/login": b">Any800v"
        }
        for path in check_map:
            url = target + path
            conn = http_req(url)
            if check_map[path] in conn.content:
                self.logger.success("found {} {}".format(self.app_name, url))
                return url
