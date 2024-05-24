import re
from requests_ntlm import HttpNtlmAuth
from xing.core.BasePlugin import BasePlugin
from xing.utils import http_req, get_logger
from xing.core import PluginType, SchemeType


class Plugin(BasePlugin):
    def __init__(self):
        super(Plugin, self).__init__()
        self.plugin_type = PluginType.BRUTE
        self.vul_name = "Exchange 邮件服务器弱口令"
        self.app_name = 'Exchange'
        self.scheme = [SchemeType.HTTP, SchemeType.HTTPS]

        self.username_file = "username_exchange.txt"
        self.password_file = "password_exchange.txt"
        self.shuffle_auth_list = True
        self.ad_domain = None
        self.brute_fun = None

    def check_autodiscover(self):
        url = self.target + "/autodiscover/"
        conn = http_req(url)
        if conn.status_code != 401:
            return False

        url2 = self.target + "/autodiscover1337/"
        conn2 = http_req(url2)

        if conn2.status_code == 404 or conn2.status_code == 302:
            self.logger.info("found brute url {}".format(url))
            return True

    def check_ews(self):
        url = self.target + "/ews/"
        conn = http_req(url)
        if conn.status_code != 401:
            return False

        url2 = self.target + "/ews1337/"
        conn2 = http_req(url2)

        if conn2.status_code == 404 or conn2.status_code == 302:
            self.logger.info("found brute url {}".format(url))
            return True

    def login_autodiscover(self, user, pwd):
        url = self.target + "/autodiscover/test.xml"
        conn = http_req(url, 'get', auth=HttpNtlmAuth(user, pwd))

        if conn.status_code == 200 and '<Autodiscover' in conn.text and "microsoft" in conn.text:
            return True

    def login_owa(self, user, pwd):
        data = {
            'destination': '%s' % self.target,
            'flags': '4',
            'forcedownlevel': '0',
            'username': '%s\%s' % (self.ad_domain, user),
            'password': pwd,
            'isUtf8': '1',
            'passwordText': ''
        }
        url = self.target + "/owa/auth.owa"
        conn = http_req(url, 'post', data=data)

        cookies_keys = [
            'cadata',
            'cadataTTL',
            'cadataKey',
            'cadataIV',
            'cadataSig'
        ]
        set_cookies = conn.headers.get('Set-Cookie')

        if conn.status_code == 302 and set_cookies:
            cnt = 0
            for cookie in cookies_keys:
                if cookie + "=" in set_cookies:
                    cnt += 1

            if cnt >= 2:
                return True

    def login_ews(self, user, pwd):
        url = self.target + "/ews/"
        conn = http_req(url, 'get', auth=HttpNtlmAuth(user, pwd))
        if conn.status_code == 500 and "NegotiateSecurityContext" in conn.text:
            # conn.text NegotiateSecurityContext failed with for host 'test2k12.fb.com' with status 'LogonDenied'
            return True

    # NTLM 认证登录时，不能使用Burp 代理
    def login(self, target, user, passwd):
        return self.brute_fun(user, passwd)

    def check_app(self, target):
        url = target + "/owa/auth/logon.aspx"
        conn = http_req(url)
        if conn.status_code == 404:
            return False

        if b"Outlook" not in conn.content:
            return False

        if b"microsoft" not in conn.content:
            return False

        pattern = r"(([a-z0-9\-]{1,20})\.(com|com\.cn|net|gov.cn|edu\.cn|cn))"
        result = re.findall(pattern, target)
        if result:
            self.ad_domain = result[0][0]

        self.set_brute_fun()
        if self.brute_fun is None:
            self.logger.debug("Not found brute Position")
            return False

        return True

    def set_brute_fun(self):
        fun = None
        if self.check_autodiscover():
            fun = self.login_autodiscover

        elif self.check_ews():
            fun = self.login_ews

        elif self.ad_domain:
            fun = self.login_owa

        self.brute_fun = fun
