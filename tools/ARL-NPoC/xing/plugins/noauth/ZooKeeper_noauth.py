from xing.core.BasePlugin import BasePlugin
from xing.core import PluginType, SchemeType


class Plugin(BasePlugin):
    def __init__(self):
        super(Plugin, self).__init__()
        self.plugin_type = PluginType.POC
        self.vul_name = "ZooKeeper 未授权访问"
        self.app_name = 'ZooKeeper'
        self.scheme = [SchemeType.ZOOKEEPER]

    def verify(self, target):
        client = self.conn_target()
        client.send(b"envi")
        data = client.recv(128)
        self.logger.debug("<<< {}".format(data))
        client.close()
        if b'zookeeper.version=' in data:
            self.logger.success("发现 ZooKeeper 未授权访问 {}".format(self.target))
            return True
