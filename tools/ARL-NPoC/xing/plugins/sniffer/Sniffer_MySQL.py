from xing.core import PluginType, SchemeType
from xing.core.BasePlugin import BasePlugin
from xing.utils import http_req, get_logger
import re
import socket


class Plugin(BasePlugin):
    def __init__(self):
        super(Plugin, self).__init__()
        self.plugin_type = PluginType.SNIFFER
        self.default_port = [3306]
        self.target_scheme = SchemeType.MYSQL

    '''
    参考 https://github.com/y1ng1996/F-Scrack/blob/master/F-Scrack.py
    '''

    def sniffer(self, host, port):
        client = socket.socket()
        client.settimeout(4)
        client.connect((host, port))
        data = client.recv(256)
        client.close()

        self.logger.debug("recv <<< {}".format(data))

        pattern = rb'^.\x00\x00\x00.*?mysql|^.\x00\x00\x00\n|.*?MariaDB server'
        matches = re.findall(pattern, data)
        if matches:
            return self.target_scheme

        return False

