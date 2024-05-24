from xing.core import PluginType, SchemeType
from xing.core.BasePlugin import BasePlugin
from xing.utils import http_req, get_logger
import socket
import time
class Plugin(BasePlugin):
    def __init__(self):
        super(Plugin, self).__init__()
        self.plugin_type = PluginType.SNIFFER
        self.default_port = [4506]
        self.target_scheme = SchemeType.ZMTP

    def sniffer(self, host, port):
        scheme_ack = b'\xff\x00\x00\x00\x00\x00\x00\x00\x01\x7f'
        check = b"\xff\x00\x00\x00\x00\x00\x00\x00\x01\x7f\x03"
        client = socket.socket()
        client.settimeout(4)
        client.connect((host, port))
        client.send(scheme_ack)
        time.sleep(0.2)
        data = client.recv(256)
        client.close()
        if len(data) >= len(check) and data[:len(check)] == check:
            return self.target_scheme
        return False

