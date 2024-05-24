import re
import os
from base64 import b64encode
from xing.utils.domain import get_fld
from xing.core.ServiceBrutePlugin import ServiceBrutePlugin
from xing.core import PluginType, SchemeType


class Plugin(ServiceBrutePlugin):
    def __init__(self):
        super(Plugin, self).__init__()
        self.plugin_type = PluginType.BRUTE
        self.vul_name = "IMAP 弱口令"
        self.app_name = 'IMAP'
        self.scheme = [SchemeType.IMAP]
        self.brute_mail_domain = ""
        self.username_file = "username_imap.txt"
        self.password_file = "password_imap.txt"

    def _imap_send(self, client, command, success_str):
        client.send(command)
        recv = self._recv_data(client)
        if not re.findall(rb'%s' % (success_str.encode()), recv):
            raise Exception("Error on {} {}".format(command, recv.decode()))
        return recv

    # 接收全部数据
    def _recv_data(self, client):
        # 结束位置判断字符
        str_list = [" BAD ", " OK ", " NO "]
        data = b''
        while True:
            recv_data = client.recv(1)
            if not recv_data:
                break
            data += recv_data

            if data.endswith(b'\r\n'):
                if re.findall(rb'(\r\n\d|^\*) OK |^\+ ', data):
                    break
                for item in str_list:
                    if item.encode() in data:
                        return data
        return data

    def _auth_login(self, user, passwd):
        client = self.conn_target(20)
        self._recv_data(client)
        self._imap_send(client, b'1 CAPABILITY\r\n', '^\* ')
        self._imap_send(client, b'2 AUTHENTICATE LOGIN\r\n', '^\+ ')
        self._imap_send(client, b64encode(user.encode()) + b'\r\n', '^\+ ')
        data = self._imap_send(client, b64encode(passwd.encode()) + b'\r\n', '^\* ')
        client.close()
        if b' OK ' in data:
            return True

    def _auth_plain(self, user, passwd):
        client = self.conn_target(20)
        self._recv_data(client)
        data = self._imap_send(client, b'1 LOGIN %s %s\r\n' % (user.encode(), passwd.encode()), ' OK | NO ')
        client.close()
        if b' OK ' in data:
            return True

    def login(self, target, user, passwd):
        user = "{}@{}".format(user, self.brute_mail_domain)
        if self.auth == "LOGIN":
            if self._auth_login(user, passwd):
                return True
        elif self.auth == "PLAIN":
            if self._auth_plain(user, passwd):
                return True
        else:
            if self._auth_plain(user, passwd):
                return True

    def check_app(self, target):
        self.auth = None
        client = self.conn_target(20)
        result = self._recv_data(client)
        client.close()
        if re.findall(rb'\* OK ', result):
            self.set_brute_mail_domain()

            if b"AUTH=LOGIN" in result:
                self.auth = "LOGON"
                return True
            if b"AUTH=PLAIN" in result:
                self.auth = "PLAIN"
                return True
            return True

    def set_brute_mail_domain(self):
        if not self.brute_mail_domain:
            fld_domain = get_fld(self.target_info["host"])
            if fld_domain:
                self.brute_mail_domain = fld_domain

        if os.getenv('BRUTE_MAIL_DOMAIN'):
            self.brute_mail_domain = os.getenv('BRUTE_MAIL_DOMAIN')
            self.logger.debug("get smtp domain {} from env".format(self.brute_mail_domain))
