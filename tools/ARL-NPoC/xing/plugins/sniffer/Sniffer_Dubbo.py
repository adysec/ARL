from xing.core import PluginType, SchemeType
from xing.core.BasePlugin import BasePlugin
import socket
import time
class Plugin(BasePlugin):
    def __init__(self):
        super(Plugin, self).__init__()
        self.plugin_type = PluginType.SNIFFER
        self.default_port = [20880]
        self.target_scheme = SchemeType.DUBBO

    def sniffer(self, host, port):
        scheme_ack = b'kjaz\r\n'
        check = b"Unsupported command: kjaz\r\ndubbo>"
        client = socket.socket()
        client.settimeout(4)
        client.connect((host, port))
        client.send(scheme_ack)
        time.sleep(0.2)
        data = client.recv(256)
        client.close()
        if len(data) >= len(check) and data[:len(check)] == check:
            return self.target_scheme
        return False

