import os
import re
from base64 import b64encode
from xing.utils.domain import get_fld
from xing.core.ServiceBrutePlugin import ServiceBrutePlugin
from xing.core import PluginType, SchemeType


class Plugin(ServiceBrutePlugin):
    def __init__(self):
        super(Plugin, self).__init__()
        self.plugin_type = PluginType.BRUTE
        self.vul_name = "SMTP 弱口令"
        self.app_name = 'SMTP'
        self.scheme = [SchemeType.SMTP]
        self.smtp_domain = ""  # 用来记录当前邮箱域名后缀
        self.username_file = "username_smtp.txt"
        self.password_file = "password_smtp.txt"

    def _smtp_send(self, client, command, success_str):
        client.send(command)
        recv = self._recv_data(client)
        if success_str not in recv:
            if b'235 ' != success_str:
                raise Exception("Error on {} {}".format(command, recv.decode()))
        return recv

    # 接收全部数据
    def _recv_data(self, client):
        data = b''
        while True:
            recv_data = client.recv(1)
            if not recv_data:
                break
            data += recv_data

            if data.endswith(b'\r\n'):
                if re.findall(rb'^\d+ |\r\n\d+ ', data):
                    break
        return data

    def login(self, target, user, passwd):
        if self.smtp_domain:
            user = "{}@{}".format(user, self.smtp_domain)

        client = self.conn_target(20)
        self._recv_data(client)
        self._smtp_send(client, b'EHLO test\r\n', b'250 ')
        self._smtp_send(client, b'AUTH LOGIN\r\n', b'334 ')
        self._smtp_send(client, b64encode(user.encode()) + b'\r\n', b'334 ')
        data = self._smtp_send(client, b64encode(passwd.encode()) + b'\r\n', b'235 ')
        client.close()
        if b'Authentication successful' in data:
            return True

    def check_app(self, target):
        client = self.conn_target(20)
        result = self._recv_data(client)
        client.close()
        if re.findall(rb'^220 ', result):
            fld_domain = self._get_domain(result)
            if fld_domain:
                self.smtp_domain = fld_domain
                self.logger.info("get smtp domain {} from {}".format(self.smtp_domain, target))

            if not self.smtp_domain:
                fld_domain = get_fld(self.target_info["host"])
                if fld_domain:
                    self.smtp_domain = fld_domain

            if os.getenv('BRUTE_MAIL_DOMAIN'):
                self.smtp_domain = os.getenv('BRUTE_MAIL_DOMAIN')
                self.logger.debug("get smtp domain {} from env".format(self.smtp_domain))

            return True

    def _get_domain(self, result_bytes):
        """
        用于从SMTP捂手信息中提取域名拼接用户名进行爆破
        """
        results = re.findall(r"220 ([^\s]+) ", result_bytes.decode())
        if results:
            fld = get_fld(results[0])
            return fld
