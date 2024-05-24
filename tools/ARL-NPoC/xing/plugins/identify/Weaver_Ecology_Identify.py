from xing.core.BasePlugin import BasePlugin
from xing.utils import http_req
from xing.core import PluginType, SchemeType


class Plugin(BasePlugin):
    def __init__(self):
        super(Plugin, self).__init__()
        self.plugin_type = PluginType.POC
        self.vul_name = "发现泛微 Ecology"
        self.app_name = 'Ecology'
        self.scheme = [SchemeType.HTTP, SchemeType.HTTPS]

    def verify(self, target):
        url = target + "/help/sys/help.html"
        if b'$(this).attr("src","image/btn_help_click' in http_req(url).content:
            self.logger.success("found Ecology {}".format(url))
            return True

        url = target + "/js"
        set_cookie = http_req(url).headers.get('Set-Cookie', "")

        if "ecology_JSessionid" in set_cookie:
            self.logger.success("found Ecology {}".format(url))
            return True
        else:
            return False
