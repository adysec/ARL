import re
from xing.core import PluginType, SchemeType
from xing.core.BasePlugin import BasePlugin
import socket

class Plugin(BasePlugin):
    def __init__(self):
        super(Plugin, self).__init__()
        self.plugin_type = PluginType.SNIFFER
        self.default_port = [22]
        self.target_scheme = SchemeType.SSH

    def sniffer(self, host, port):
        payload = rb'^[sS][sS][hH]-[12]\.'

        sock = socket.socket()
        sock.settimeout(4)
        sock.connect((host, port))
        recv_data = sock.recv(256)
        sock.close()
        if re.findall(payload, recv_data):
            return self.target_scheme

        return False

