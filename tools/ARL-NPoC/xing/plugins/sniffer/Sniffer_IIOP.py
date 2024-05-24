from xing.core import PluginType, SchemeType
from xing.core.BasePlugin import BasePlugin
import socket


class Plugin(BasePlugin):
    def __init__(self):
        super(Plugin, self).__init__()
        self.plugin_type = PluginType.SNIFFER
        self.default_port = [7001]
        self.target_scheme = SchemeType.IIOP

    def sniffer(self, host, port):
        ack_hexstr = '47494f50010200030000001700000002000000000000000b4e616d6553657276696365'
        scheme_ack = bytes.fromhex(ack_hexstr)
        check = b"GIOP"
        client = socket.socket()
        client.settimeout(4)
        client.connect((host, port))
        client.send(scheme_ack)
        data = client.recv(256)
        client.close()
        if len(data) >= 4 and data[:4] == check:
            if b"weblogic/corba" in data or b'omg.org/CosNaming' in data:
                return self.target_scheme
        return False

