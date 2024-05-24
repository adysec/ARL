import importlib.util
import os
from xing.conf import Conf
from xing.utils import get_logger

def import_source(spec, path):
    module_spec = importlib.util.spec_from_file_location(spec, path)
    module = importlib.util.module_from_spec(module_spec)
    module_spec.loader.exec_module(module)
    return module


def walk_py(path):
    for dir_path, dir_names, filenames in os.walk(path):
        if dir_path.endswith("__pycache__"):
            continue

        for f in filenames:
            if f.startswith('_'):
                continue

            split = f.split('.')

            if len(split) == 2 and split[1] == 'py':
                abspath = os.path.abspath(os.path.join(dir_path, f))
                yield abspath, split[0]


def load_plugins(path):
    logger = get_logger()
    plugins = []
    for file_path, name in walk_py(path):
        try:
            module = import_source(spec="xing_plugins", path=file_path)
            Plugin = getattr(module, 'Plugin')
            plugin = Plugin()
            setattr(plugin, '_plugin_name', name)
            plugins.append(plugin)
        except Exception as e:
            logger.warning("load plugin error from {}".format(file_path))
            logger.exception(e)

    return plugins


def load_all_plugin():
    paths = [Conf.SYSTEM_PLUGINS_DIR]
    if Conf.USER_PLUGINS_DIR:
        paths.append(Conf.USER_PLUGINS_DIR)

    plugins = []
    for path in paths:
        plugins.extend(load_plugins(path))

    return plugins