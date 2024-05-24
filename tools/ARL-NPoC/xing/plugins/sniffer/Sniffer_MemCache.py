from xing.core import PluginType, SchemeType
from xing.core.BasePlugin import BasePlugin
from xing.utils import http_req, get_logger
import socket

class Plugin(BasePlugin):
    def __init__(self):
        super(Plugin, self).__init__()
        self.plugin_type = PluginType.SNIFFER
        self.default_port = [11211]
        self.target_scheme = SchemeType.MEMCACHED

    def sniffer(self, host, port):
        scheme_ack = b'memcache\r\n'
        check = b'ERROR\r\n'
        client = socket.socket()
        client.settimeout(4)
        client.connect((host, port))
        client.send(scheme_ack)
        data = client.recv(256)
        client.close()
        if len(data) >= 7 and data[:7] == check:
            return self.target_scheme
        return False

