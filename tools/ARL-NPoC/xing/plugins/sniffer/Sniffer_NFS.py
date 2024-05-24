import re
from xing.core import PluginType, SchemeType
from xing.core.BasePlugin import BasePlugin
import socket

class Plugin(BasePlugin):
    def __init__(self):
        super(Plugin, self).__init__()
        self.plugin_type = PluginType.SNIFFER
        self.default_port = [2049]
        self.target_scheme = SchemeType.NFS

    def sniffer(self, host, port):
        scheme_ack = b'\x80\0\0\x22\x23\x24\x25\x13\0\0\0\0\0\0\0\x02\0\x01\x86\xA0\0\x01\x97\x7C\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0'
        client = socket.socket()
        client.settimeout(4)
        client.connect((host, port))
        client.send(scheme_ack)
        data = client.recv(256)
        client.close()

        check = b'\x80\x00\x00\x10#$%\x13\x00\x00'
        if len(data) >= len(check) and data[:len(check)] == check:
            return self.target_scheme

        return False


