from xing.core.BasePlugin import BasePlugin
from xing.utils import http_req, get_logger
from xing.core import PluginType, SchemeType


class Plugin(BasePlugin):
    def __init__(self):
        super(Plugin, self).__init__()
        self.plugin_type = PluginType.POC
        self.vul_name = "发现 Apache Shiro"
        self.app_name = 'Shiro'
        self.scheme = [SchemeType.HTTP, SchemeType.HTTPS]

    def verify(self, target):
        url = target + "/"
        headers = {
            "Cookie": "rememberMe=1"
        }

        set_cookie = http_req(url, headers=headers).headers.get('Set-Cookie', "")

        if "rememberMe=deleteMe" in set_cookie:
            self.logger.success("found shiro {}".format(target))
            return True
        else:
            return False
