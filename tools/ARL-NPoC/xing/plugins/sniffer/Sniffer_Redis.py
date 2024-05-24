from xing.core import PluginType, SchemeType
from xing.core.BasePlugin import BasePlugin
from xing.utils import http_req, get_logger
import socket

class Plugin(BasePlugin):
    def __init__(self):
        super(Plugin, self).__init__()
        self.plugin_type = PluginType.SNIFFER
        self.default_port = [6379]
        self.target_scheme = SchemeType.REDIS

    def sniffer(self, host, port):
        scheme_ack = b'help\r\n'
        check1 = b"-ERR unknown command"
        check2 = b'-NOAUTH Authentication required'
        client = socket.socket()
        client.settimeout(4)
        client.connect((host, port))
        client.send(scheme_ack)
        data = client.recv(256)
        client.close()
        
        if len(data) >= len(check1) and data[:len(check1)] == check1:
            return self.target_scheme
        if len(data) >= len(check2) and check2 in data:
            return self.target_scheme
        return False

