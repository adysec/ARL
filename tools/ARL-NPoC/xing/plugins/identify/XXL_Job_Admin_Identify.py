from xing.core.BasePlugin import BasePlugin
from xing.utils import http_req, get_logger
from xing.core import PluginType, SchemeType


class Plugin(BasePlugin):
    def __init__(self):
        super(Plugin, self).__init__()
        self.plugin_type = PluginType.POC
        self.vul_name = "发现 xxl-job-admin"
        self.app_name = 'xxl-job-admin'
        self.scheme = [SchemeType.HTTP, SchemeType.HTTPS]

    def verify(self, target):
        path_list = ["/toLogin", "/xxl-job/toLogin", "/xxl-job-admin/toLogin", "/xxl/toLogin", "/xxljob/toLogin"]
        check = b"<b>XXL</b>JOB"
        for path in path_list:
            url = target + path
            conn = http_req(url)
            if check in conn.content:
                self.logger.success("found {} {}".format(self.app_name, url))
                return url
