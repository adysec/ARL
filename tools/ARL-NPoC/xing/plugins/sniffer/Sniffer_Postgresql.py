from xing.core import PluginType, SchemeType
from xing.core.BasePlugin import BasePlugin
import socket

class Plugin(BasePlugin):
    def __init__(self):
        super(Plugin, self).__init__()
        self.plugin_type = PluginType.SNIFFER
        self.default_port = [5432]
        self.target_scheme = SchemeType.POSTGRESQL

    def sniffer(self, host, port):
        scheme_ack = b'\x00\x00\x00\x08\x04\xd2\x16\x2f'
        client = socket.socket()
        client.settimeout(4)
        client.connect((host, port))
        client.send(scheme_ack)
        data = client.recv(256)
        client.close()
        if len(data) == 1 and data in [b'N', b'S']:
            return self.target_scheme
        return False

