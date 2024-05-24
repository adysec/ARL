from xing.core.BasePlugin import BasePlugin
from xing.utils import http_req, get_logger
from xing.core import PluginType, SchemeType


# header="X-ClickHouse-Summary"
class Plugin(BasePlugin):
    def __init__(self):
        super(Plugin, self).__init__()
        self.plugin_type = PluginType.POC
        self.vul_name = "发现 Clickhouse REST API"
        self.app_name = 'Clickhouse'
        self.scheme = [SchemeType.HTTP, SchemeType.HTTPS]

    def verify(self, target):
        url = target + "/ping"
        conn = http_req(url)
        clickhouse_summary = conn.headers.get('X-ClickHouse-Summary', "")

        if "read_rows" not in clickhouse_summary:
            return

        if b'Ok.' in conn.content:
            self.logger.success("found {} {}".format(self.app_name, url))
            return True
