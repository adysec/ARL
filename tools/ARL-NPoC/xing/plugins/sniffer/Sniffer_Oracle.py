from xing.core import PluginType, SchemeType
from xing.core.BasePlugin import BasePlugin
from xing.utils import http_req, get_logger
import socket

class Plugin(BasePlugin):
    def __init__(self):
        super(Plugin, self).__init__()
        self.plugin_type = PluginType.SNIFFER
        self.default_port = [1521]
        self.target_scheme = SchemeType.ORACLE

    def sniffer(self, host, port):
        check = b"(DESCRIPTION=(TMP=)(VSNNUM="
        scheme_ack = b"\x00Z\x00\x00\x01\x00\x00\x00\x016\x01,\x00\x00"
        scheme_ack += b"\x08\x00\x7f\xff\x7f\x08\x00\x00\x00\x01\x00 \x00:"
        scheme_ack += b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
        scheme_ack += b"\x00\x00\x004\xe6\x00\x00\x00\x01\x00\x00\x00\x00\x00"
        scheme_ack += b"\x00\x00\x00(CONNECT_DATA=(COMMAND=version))"

        client = socket.socket()
        client.settimeout(4)
        client.connect((host, port))
        client.send(scheme_ack)
        data = client.recv(256)
        client.close()
        if check in data:
            return self.target_scheme
        return False

