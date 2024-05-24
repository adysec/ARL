from xing.core import PluginType, SchemeType
from xing.core.BasePlugin import BasePlugin
from xing.utils import http_req, get_logger
import socket
from struct import Struct

class Plugin(BasePlugin):
    def __init__(self):
        super(Plugin, self).__init__()
        self.plugin_type = PluginType.SNIFFER
        self.default_port = [27017]
        self.target_scheme = SchemeType.MONGODB

    def sniffer(self, host, port):
        ack_hexstr = "3f0000001400000000000000d40700000400000061646d696e2e24636d640000000000ffffffff18000000106c697374446174616261736573000100000000"
        scheme_ack = bytes.fromhex(ack_hexstr)
        client = socket.socket()
        client.settimeout(4)
        client.connect((host, port))
        client.send(scheme_ack)
        data = client.recv(256)
        client.close()

        r = Struct('<iiii')
        if len(data) < r.size:
            return False

        _, _, rid, opcode = r.unpack(data[:r.size])

        if rid == 20 and opcode == 1:
            return self.target_scheme
        return False

