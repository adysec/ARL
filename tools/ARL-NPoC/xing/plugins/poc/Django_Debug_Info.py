from xing.core.BasePlugin import BasePlugin
from xing.utils import http_req
from xing.core import PluginType, SchemeType


class Plugin(BasePlugin):
    def __init__(self):
        super(Plugin, self).__init__()
        self.plugin_type = PluginType.POC
        self.vul_name = "Django 开启调试模式"
        self.app_name = 'Django'
        self.scheme = [SchemeType.HTTPS, SchemeType.HTTP]

    def verify(self, target):
        paths = ["/lljfafd", "/api/lljfafd"]
        for path in paths:
            url = target + path
            conn = http_req(url)
            content = conn.content
            if conn.status_code != 404:
                continue

            if b"Django" not in content or b"DEBUG = True" not in content:
                self.logger.debug("not found Django")
                continue

            if b"<title>Page not found at" in content and b"lljfafd</title>" in content:
                self.logger.success("发现 Django 开启调试模式 {}".format(self.target))
                return url
