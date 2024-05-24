from xing.core import PluginType, SchemeType
from xing.core.BasePlugin import BasePlugin
from xing.utils import http_req, get_logger
import socket
import re

class Plugin(BasePlugin):
    def __init__(self):
        super(Plugin, self).__init__()
        self.plugin_type = PluginType.SNIFFER
        self.default_port = [143]
        self.target_scheme = SchemeType.IMAP

    def sniffer(self, host, port):
        payload = rb'^\*\sOK\s\['

        sock = socket.socket()
        sock.settimeout(4)
        sock.connect((host, port))
        recv_data = sock.recv(256)
        if re.findall(payload, recv_data):
            return self.target_scheme

        return False
