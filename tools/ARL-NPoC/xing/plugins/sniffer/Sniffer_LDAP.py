from xing.core import PluginType, SchemeType
from xing.core.BasePlugin import BasePlugin
from xing.utils import http_req, get_logger
import socket

class Plugin(BasePlugin):
    def __init__(self):
        super(Plugin, self).__init__()
        self.plugin_type = PluginType.SNIFFER
        self.default_port = [389]
        self.target_scheme = SchemeType.LDAP

    def sniffer(self, host, port):
        check = b'0\r\x02\x02\x01\x06a\x07\n'
        scheme_ack = b"\x30\x84\x00\x00\x00\x11\x02\x02\x01\x06\x60\x84\x00\x00\x00\x07"
        scheme_ack += b"\x02\x01\x03\x04\x00\x80\x00"
        client = socket.socket()
        client.settimeout(4)
        client.connect((host, port))
        client.send(scheme_ack)
        data = client.recv(256)
        client.close()
        if len(data) >= len(check) and data[:len(check)] == check:
            return self.target_scheme
        return False

