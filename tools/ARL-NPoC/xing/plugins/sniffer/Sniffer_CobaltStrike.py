from xing.core import PluginType, SchemeType
from xing.core.BasePlugin import BasePlugin
import ssl

class Plugin(BasePlugin):
    def __init__(self):
        super(Plugin, self).__init__()
        self.plugin_type = PluginType.SNIFFER
        self.default_port = [50050]
        self.target_scheme = SchemeType.COBALT_STRIKE

    def sniffer(self, host, port):
        data = self._login_cs("ThisIsNotAValidPassword")
        self.logger.debug("recv <<< {}".format(data))

        if data == b'\x00\x00\xca\xfe' or data == b'\x00\x00\x00\x00':
            return self.target_scheme

        return False

    def _login_cs(self, pwd):
        payload = self.gen_payload(pwd)
        sock = self.conn_target()
        ssl_ctx = ssl.SSLContext()
        ssl_sock = ssl_ctx.wrap_socket(sock)
        ssl_sock.send(payload)

        resp = b''
        while len(resp) < 4:
            data = ssl_sock.recv(4)
            if len(data) < 1:
                break
            resp += data

        ssl_sock.close()
        return resp

    def gen_payload(self, pwd):
        payload = bytearray(
            b'\x00\x00\xbe\xef' +
            len(pwd).to_bytes(1, 'big', signed=True) +
            bytes(bytes(pwd, 'ascii').ljust(256, b'M'))
        )

        return payload
