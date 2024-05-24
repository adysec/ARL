import os
from xing.conf import Conf
from xing.core import PluginType, DEFAULT_PORT_SCHEME_LIST
from xing.utils import parse_target_info, get_logger, load_file
import socket

class BasePlugin:
    def __init__(self):
        self._target_info = None
        self.logger = get_logger()
        self.do_map = {
            PluginType.POC: self.do_verify,
            PluginType.SNIFFER: self.do_sniffer,
            PluginType.BRUTE: self.do_brute
        }
        self.target = None
        self.plugin_type = None
        self.target_scheme = None
        self.default_port = []
        self.username_file = None
        self.password_file = None
        self.app_name = None
        self.scheme = None
        self.vul_name = None
        self.interact = False

    def verify(self, target):
        """
        PoC插件，用来判断漏洞是否存在
        """
        raise NotImplementedError()

    def sniffer(self, host, port):
        """
        协议识别插件，用来识别协议
        """
        raise NotImplementedError()

    def login(self, target, user, passwd):
        """
        爆破插件中用来登录
        """
        raise NotImplementedError()

    def check_app(self, target):
        """
        爆破插件中用来判断是否是目标应用
        """
        raise NotImplementedError()


    def set_target(self, target):
        self._target_info = None
        if ":" not in target and self.plugin_type == PluginType.SNIFFER:
            target = "{}:{}".format(target, self.default_port[0])
        self.target = target

    def do_verify(self):
        results = self.verify(self.target)
        return results

    def do_brute(self):
        from xing.core import brute_runner
        service_brute_fun = getattr(self, "service_brute", None)
        result_map = {}
        if service_brute_fun and callable(service_brute_fun):
            brute_ret = service_brute_fun()
            if not brute_ret:
                return
            result_map[brute_ret["username"]] = brute_ret["password"]

        else:
            self.logger.info("start brute {} {}".format(self.app_name, self.target))
            if not self.check_app(target=self.target):
                return

            self.logger.info("found {} {}".format(self.app_name, self.target))

            user_list, pass_list = self.load_dict()
            self.logger.info("load auth pair {}".format(len(user_list)))

            result_map = brute_runner(plg=self, target=self.target,
                         username_list=user_list, password_list=pass_list, concurrency=6)

        for user in result_map:
            self.logger.success("found weak pass {}:{} {}".format(user, result_map[user], self.target))
        return result_map

    def load_dict(self):
        dict_dir = os.path.join(Conf.PROJECT_DIRECTORY, "dicts")
        user_file = os.path.join(dict_dir, self.username_file)
        pwd_file = os.path.join(dict_dir, self.password_file)

        self.logger.debug("username_file -> {}".format(self.username_file))
        self.logger.debug("password_file -> {}".format(self.password_file))

        user = load_file(user_file)

        """获取确定的用户名密码"""
        gen_users_fun = getattr(self, "gen_users", None)
        if gen_users_fun:
            self.logger.info("gen user {} {}".format(self.target, self))
            _gen_users = gen_users_fun()
            self.logger.info("get user {} {} {}".format(len(_gen_users), self.target, self))
            if _gen_users:
                user = _gen_users

        pwd = set(load_file(pwd_file))
        user_list = []
        pass_list = []
        for u in user:
            u = u.strip()
            for p in self._pwd_gen(u, pwd):
                user_list.append(u)
                pass_list.append(p)

        return user_list, pass_list

    def _pwd_gen(self, user, pass_list):
        pwd_set = set()
        for p in pass_list:
            p = p.strip()
            new_pwd = p.replace('%user%', user)
            pwd_set.add(new_pwd)

        return pwd_set

    def should_skip(self):
        if self.plugin_type == PluginType.SNIFFER:
            if self.target_scheme in DEFAULT_PORT_SCHEME_LIST:
                if self.target_info['port'] not in self.default_port:
                    return True

        if self.plugin_type != PluginType.SNIFFER:
            if self.target_info["scheme"] not in self.scheme:
                return True
        return False

    def do_sniffer(self):
        host = self.target_info['host']
        port = self.target_info['port']
        results = self.sniffer(host, port)
        if results:
            uri = "{}://{}:{}".format(results, host, port)
            self.logger.success("found {}".format(uri))
            return uri
        return results

    def run(self):
        target = self.target_info['target']
        plugin_name = getattr(self, '_plugin_name', None)
        try:
            if self.should_skip():
                self.logger.debug("skip [{}] {}".format(plugin_name, target))
                return
            do_action = self.do_map[self.plugin_type]
            return do_action()
        except Exception as e:
            error = self.target
            if self.plugin_type == PluginType.SNIFFER:
                error = self.target_info['raw_target']

            if self.plugin_type == PluginType.SNIFFER:
                self.logger.debug("[{}] {} {} ".format(
                    plugin_name, error, e))
            else:
                self.logger.warning("[{}] {} {} ".format(
                    plugin_name, error, e))

            if isinstance(e, OSError):
                return
            self.logger.exception(e)

    @property
    def target_info(self):
        if self._target_info:
            return self._target_info

        raw_target = self.target
        if self.plugin_type != PluginType.SNIFFER and "://" not in self.target:
            self.target = self.scheme[0] + "://" + self.target

        target_info = parse_target_info(self.target)
        target_info['raw_target'] = raw_target

        self.target = target_info['target']
        self._target_info = target_info

        return self._target_info

    def __str__(self):
        return getattr(self, '_plugin_name', "")

    def conn_target(self, timeout=4):
        """
        连接到目标, 请调用后一定要手动close
        """

        host = self.target_info["host"]
        port = self.target_info["port"]
        client = socket.socket()
        client.settimeout(timeout)
        client.connect((host, port))

        return client
