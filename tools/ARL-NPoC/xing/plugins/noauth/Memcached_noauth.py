from xing.core.BasePlugin import BasePlugin
from xing.core import PluginType, SchemeType


class Plugin(BasePlugin):
    def __init__(self):
        super(Plugin, self).__init__()
        self.plugin_type = PluginType.POC
        self.vul_name = "Memcached 未授权访问"
        self.app_name = 'Memcached'
        self.scheme = [SchemeType.MEMCACHED]

    def verify(self, target):
        client = self.conn_target()
        client.send(b"stats\r\n")
        data = client.recv(128)
        self.logger.debug("<<< {}".format(data))
        client.close()
        if b'STAT version' in data:
            self.logger.success("发现 Memcached 未授权访问 {}".format(self.target))
            return True
