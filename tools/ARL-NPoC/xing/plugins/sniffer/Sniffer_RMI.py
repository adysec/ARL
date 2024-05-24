from xing.core import PluginType, SchemeType
from xing.core.BasePlugin import BasePlugin
from xing.utils import http_req, get_logger
import socket

class Plugin(BasePlugin):
    def __init__(self):
        super(Plugin, self).__init__()
        self.plugin_type = PluginType.SNIFFER
        self.default_port = [1099]
        self.target_scheme = SchemeType.RMI

    def sniffer(self, host, port):
        scheme_ack = b'JRMI\x00\x02K'
        check = b"N\x00"
        client = socket.socket()
        client.settimeout(4)
        client.connect((host, port))
        client.send(scheme_ack)
        data = client.recv(256)
        client.close()
        if len(data) >= 4 and data[:2] == check:
            return self.target_scheme
        return False

