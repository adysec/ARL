import re
from xing.core import PluginType, SchemeType
from xing.core.BasePlugin import BasePlugin
import socket

class Plugin(BasePlugin):
    def __init__(self):
        super(Plugin, self).__init__()
        self.plugin_type = PluginType.SNIFFER
        self.default_port = [873]
        self.target_scheme = SchemeType.RSYNC

    def sniffer(self, host, port):
        payload = rb'^@RSYNCD:\s+\d+.\d+\n'

        client = socket.socket()
        client.settimeout(4)
        client.connect((host, port))
        recv_data = client.recv(256)
        client.close()

        if re.findall(payload, recv_data):
            return self.target_scheme

        return False

