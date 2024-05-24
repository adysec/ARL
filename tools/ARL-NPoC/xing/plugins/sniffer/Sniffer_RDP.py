from xing.core import PluginType, SchemeType
from xing.core.BasePlugin import BasePlugin
from xing.utils import http_req, get_logger
import socket
import re

class Plugin(BasePlugin):
    def __init__(self):
        super(Plugin, self).__init__()
        self.plugin_type = PluginType.SNIFFER
        self.default_port = [3389]
        self.target_scheme = SchemeType.RDP

    def sniffer(self, host, port):
        data = """03 00 00 2f 2a e0 00 00  00 00 00 43 6f 6f 6b 69
                    65 3a 20 6d 73 74 73 68  61 73 68 3d 61 64 6d 69
                    6e 69 73 74 72 0d 0a 01  00 08 00 03 00 00 00"""
        payload = rb'^(.{5}\xd0|.*McDn)'

        data = data.replace(" ", "").replace("\r", "").replace("\n", "")
        data = bytes.fromhex(data)
        sock = socket.socket()
        sock.settimeout(4)
        sock.connect((host, port))
        sock.send(data)
        recv_data = sock.recv(256)
        sock.close()
        if re.findall(payload, recv_data):
            return self.target_scheme

        return False
