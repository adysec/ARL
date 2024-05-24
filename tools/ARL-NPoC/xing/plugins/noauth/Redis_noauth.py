from xing.core.BasePlugin import BasePlugin
from xing.core import PluginType, SchemeType


class Plugin(BasePlugin):
    def __init__(self):
        super(Plugin, self).__init__()
        self.plugin_type = PluginType.POC
        self.vul_name = "Redis 未授权访问"
        self.app_name = 'Redis'
        self.scheme = [SchemeType.REDIS]

    def verify(self, target):
        client = self.conn_target()
        client.send(b"info\r\n")
        data = client.recv(200)
        self.logger.debug("<<< {}".format(data))
        client.close()
        if data.startswith(b'$') and b'redis_version:' in data:
            self.logger.success("发现 Redis 未授权访问 {}".format(self.target))
            return True
