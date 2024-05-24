from xing.core import PluginType, SchemeType
from xing.core.BasePlugin import BasePlugin
from xing.utils import http_req, get_logger
import socket

class Plugin(BasePlugin):
    def __init__(self):
        super(Plugin, self).__init__()
        self.plugin_type = PluginType.SNIFFER
        self.default_port = [1090]
        self.target_scheme = SchemeType.SOCKS4

    def sniffer(self, host, port):
        scheme_ack = b'\x04\x01\x00\x50\x01\x01\x01\x01\x00'
        client = socket.socket()
        client.settimeout(4)
        client.connect((host, port))
        client.send(scheme_ack)
        data = client.recv(255)
        client.close()

        if len(data) != 8:
            return False

        # \x5a 90 表示无密码
        """
        protocol=socks4 && banner="0x5a"
        0x5A	请求已批准
        0x5B	请求被拒绝或失败
        0x5C	请求失败，因为客户端未以identd运行（或无法从服务器访问）
        0x5D	请求失败，因为客户端的身份无法确认请求中的用户ID
        """
        if data[1] not in [90, 91, 92, 93]:
            return False

        if data[0] == 0 and data[-1] == 0:
            return self.target_scheme
        return False

