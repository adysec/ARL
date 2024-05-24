from xing.core.BaseThread import BaseThread
from xing.core.BasePlugin import BasePlugin
from xing.core import PluginType
from xing.utils import get_logger, append_file
from xing.utils.save_result import save_result



class PluginRunner(object):
    def __init__(self, plugins, targets, concurrency=6):
        self.plugins = plugins
        self.targets = targets
        self.concurrency = concurrency
        self.logger = get_logger()
        self.runner_cnt = 0

    def run(self):
        if len(self.plugins) > len(self.targets):
            cnt = 0
            count = len(self.targets)
            for target in self.targets:
                cnt += 1
                self.logger.info("[{}/{}] PluginRunner {}".format(cnt, count, target))
                runner = ConcurrentByPlugin(plugins=self.plugins,
                                            target=target, runner=self,
                                            concurrency=self.concurrency)
                runner.run()
        else:
            cnt = 0
            count = len(self.plugins)
            for plugin in self.plugins:
                cnt += 1
                self.logger.info("[{}/{}] PluginRunner {}".format(cnt, count, plugin))
                runner = ConcurrentByTarget(targets=self.targets,
                                            plugin=plugin, runner=self, concurrency=self.concurrency)
                runner.run()


def plugin_runner(plugins, targets, concurrency=6):
    runner = PluginRunner(plugins=plugins, targets=targets, concurrency=concurrency)
    return runner.run()


class Mixin(object):
    def __init__(self, *args, **kwargs):
        self.result_map = {
            PluginType.SNIFFER: [],
            PluginType.POC: []
        }

    def put_result(self, plg, target, ret):
        if plg.plugin_type == PluginType.SNIFFER:
            self.result_map[PluginType.SNIFFER].append(ret)
        else:
            if isinstance(ret, str) and "://" in ret:
                msg = ret
            else:
                msg = "{}----{}".format(target, ret)

            self.result_map[PluginType.POC].append(msg)


class ConcurrentByPlugin(BaseThread, Mixin):
    def __init__(self, plugins, target, runner, concurrency=6):
        super(ConcurrentByPlugin, self).__init__(targets=plugins, concurrency=concurrency)
        Mixin.__init__(self)
        self.target = target
        self.runner = None
        if isinstance(runner, PluginRunner):
            self.runner = runner

    def work(self, plg):
        self.runner.runner_cnt += 1
        ret = run(plg=plg, target=self.target)
        if not ret:
            return

        self.put_result(plg, self.target, ret)

    def run(self):
        self._run()


class ConcurrentByTarget(BaseThread, Mixin):
    def __init__(self, targets, plugin, runner, concurrency=6):
        super(ConcurrentByTarget, self).__init__(targets=targets, concurrency=concurrency)
        Mixin.__init__(self)
        self.plugin = plugin
        self.runner = None
        if isinstance(runner, PluginRunner):
            self.runner = runner

    def work(self, target):
        self.runner.runner_cnt += 1
        ret = run(plg=self.plugin, target=target)
        if not ret:
            return

        self.put_result(self.plugin, target, ret)

    def run(self):
        self._run()


def run(plg, target, copy_flag=True):
    if not isinstance(plg, BasePlugin):
        raise Exception("{} not xing plugin".format(plg))

    new_plg = plg
    if copy_flag:
        obj = plg.__class__()
        name = getattr(plg, '_plugin_name', "")
        setattr(obj, '_plugin_name', name)
        new_plg = obj

        setattr(obj, 'password_file', getattr(plg, 'password_file'))
        setattr(obj, 'username_file', getattr(plg, 'username_file'))

    new_plg.set_target(target)
    result = new_plg.run()
    if result and not should_skip_web_brute_result(new_plg):
        save_result(new_plg, result)

    return result


def should_skip_web_brute_result(plg):
    login_fun = getattr(plg, "login", None)
    if not login_fun:
        return False

    if not callable(login_fun):
        return False

    service_brute_fun = getattr(plg, "service_brute", None)
    if service_brute_fun and callable(service_brute_fun):
        return False

    if plg.plugin_type == PluginType.BRUTE:
        return True
    else:
        return False
