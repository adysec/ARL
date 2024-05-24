from xing.core.BasePlugin import BasePlugin
from xing.core import PluginType, SchemeType
import ssl
import time


class Plugin(BasePlugin):
    def __init__(self):
        super(Plugin, self).__init__()
        self.plugin_type = PluginType.BRUTE
        self.scheme = [SchemeType.REDIS]
        self.vul_name = "Redis 弱口令"
        self.app_name = 'Redis'
        self.password_file = "password_redis.txt"
        self.username_file = "username_redis.txt"

    def check_app(self, target):
        data = self._login_redis(b'notp12jlazz')
        self.logger.debug(data)
        check_list = [b'-ERR invalid password', b'-WRONGPASS invalid username-password pair']

        for check in check_list:
            if check in data:
                return True

    def login(self, target, user, passwd):
        data = self._login_redis(passwd)
        if b'+OK' in data:
            return True
        time.sleep(0.2)
        return False

    def _login_redis(self, pwd):
        send_data = 'auth {}\r\n'.format(pwd)
        client = self.conn_target()
        client.send(send_data.encode(encoding='UTF-8'))
        data = client.recv(200)
        client.close()

        return data
