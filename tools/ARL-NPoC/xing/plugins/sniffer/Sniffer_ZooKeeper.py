from xing.core import PluginType, SchemeType
from xing.core.BasePlugin import BasePlugin
import socket

class Plugin(BasePlugin):
    def __init__(self):
        super(Plugin, self).__init__()
        self.plugin_type = PluginType.SNIFFER
        self.default_port = [2181]
        self.target_scheme = SchemeType.ZOOKEEPER

    def sniffer(self, host, port):
        scheme_ack = b'ruok'
        client = socket.socket()
        client.settimeout(4)
        client.connect((host, port))
        client.send(scheme_ack)
        data = client.recv(256)
        client.close()
        if data == b'imok':
            return self.target_scheme
        return False

