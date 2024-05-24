from xing.core import PluginType, SchemeType
from xing.core.BasePlugin import BasePlugin
import socket

class Plugin(BasePlugin):
    def __init__(self):
        super(Plugin, self).__init__()
        self.plugin_type = PluginType.SNIFFER
        self.default_port = [8009]
        self.target_scheme = SchemeType.AJP

    def sniffer(self, host, port):
        #JK_AJP13_CPING_REQUEST
        scheme_ack = b'\x12\x34\x00\x01\x0A'
        check = b"AB\x00\x01\t"
        client = socket.socket()
        client.settimeout(4)
        client.connect((host, port))
        client.send(scheme_ack)
        data = client.recv(256)
        client.close()
        if len(data) >= len(check) and data[:len(check)] == check:
            return self.target_scheme
        return False

