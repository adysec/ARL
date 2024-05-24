import re
from xing.core import PluginType, SchemeType
from xing.core.BasePlugin import BasePlugin
from xing.utils import http_req, get_logger
import socket


class Plugin(BasePlugin):
    def __init__(self):
        super(Plugin, self).__init__()
        self.plugin_type = PluginType.SNIFFER
        self.default_port = [10809, 3128, 80]
        self.target_scheme = SchemeType.PROXY_HTTPS

    def sniffer(self, host, port):
        """HTTP/1.1 200 Connection Established"""
        scheme_ack = b'CONNECT 1.1.1.1:443 HTTP/1.1\r\nHost: 1.1.1.1:443\r\n'
        scheme_ack += b'User-Agent: ua\r\nProxy-Connection: Keep-Alive\r\n\r\n'
        check = rb"HTTP/\d.\d 200 Connection Established"
        client = socket.socket()
        client.settimeout(4)
        client.connect((host, port))
        client.send(scheme_ack)
        data = client.recv(128)
        client.close()

        if data[-4:] != b"\r\n\r\n":
            return False

        if re.findall(check, data, re.IGNORECASE):
            return self.target_scheme

        return False

