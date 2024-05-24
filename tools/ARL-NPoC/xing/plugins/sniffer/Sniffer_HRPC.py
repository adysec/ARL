from xing.core import PluginType, SchemeType
from xing.core.BasePlugin import BasePlugin
import socket
import time


class Plugin(BasePlugin):
    def __init__(self):
        super(Plugin, self).__init__()
        self.plugin_type = PluginType.SNIFFER
        self.default_port = [8032]
        self.target_scheme = SchemeType.HRPC

    def sniffer(self, host, port):
        scheme_ack = b'hrpc\x3f\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
        check = b"cannot communicate with client version 630"
        client = self.conn_target()

        client.send(scheme_ack)
        time.sleep(0.2)
        data = client.recv(256)

        self.logger.debug("recv <<< {}".format(data))

        client.close()
        if len(data) >= len(check) and check in data:
            return self.target_scheme
        return False

