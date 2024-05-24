from xing.core import PluginType, SchemeType
from xing.core.BasePlugin import BasePlugin
from xing.utils import http_req, get_logger
import socket


class Plugin(BasePlugin):
    def __init__(self):
        super(Plugin, self).__init__()
        self.plugin_type = PluginType.SNIFFER
        self.default_port = [1090]
        self.target_scheme = SchemeType.SOCKS5

    def sniffer(self, host, port):
        scheme_ack = b'\x05\x02\x00\x01'
        client = socket.socket()
        client.settimeout(4)
        client.connect((host, port))
        client.send(scheme_ack)
        data = client.recv(255)
        client.close()

        """
        protocol=socks5 && banner="0x00"
        """
        if len(data) != 2:
            return False

        self.logger.debug("receive {}".format(data))

        if data[0] == 5:
            return self.target_scheme
        return False

