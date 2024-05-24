from xing.core import PluginType, SchemeType
from xing.core.BasePlugin import BasePlugin
from xing.utils import http_req, get_logger
import socket

class Plugin(BasePlugin):
    def __init__(self):
        super(Plugin, self).__init__()
        self.plugin_type = PluginType.SNIFFER
        self.default_port = [5000, 5005]
        self.target_scheme = SchemeType.JDWP

    def sniffer(self, host, port):
        Handshake = b"JDWP-Handshake"
        client = socket.socket()
        client.settimeout(4)
        client.connect((host, port))
        client.send(Handshake)
        data = client.recv(256)
        client.close()
        if Handshake == data:
            return self.target_scheme
        return False

