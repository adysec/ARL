from xing.core import PluginType, SchemeType
from xing.core.BasePlugin import BasePlugin
from xing.utils import http_req, get_logger
import socket

class Plugin(BasePlugin):
    def __init__(self):
        super(Plugin, self).__init__()
        self.plugin_type = PluginType.SNIFFER
        self.default_port = [7001]
        self.target_scheme = SchemeType.T3

    def sniffer(self, host, port):
        scheme_ack = b't3 1.0\n\n'
        check = b"VERS:Incompatible versions - client: '1.0'"
        client = socket.socket()
        client.settimeout(4)
        client.connect((host, port))
        client.send(scheme_ack)
        data = client.recv(256)
        client.close()
        
        if len(data) >= len(check) and data[:len(check)] == check:
            return self.target_scheme
        return False

