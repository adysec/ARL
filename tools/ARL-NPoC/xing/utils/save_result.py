import json
from xing.conf import Conf
from xing.core.BasePlugin import BasePlugin
from xing.core.const import PluginType
from xing.utils.file import append_file
from xing.core.ServiceBrutePlugin import ServiceBrutePlugin


def save_result(plg, msg):
    if not isinstance(plg, BasePlugin):
        raise TypeError("BasePlugin is required")

    text_msg = ""
    if msg and isinstance(plg, ServiceBrutePlugin) and isinstance(msg, dict):
        username = list(msg)[0]
        password = msg[username]
        msg = {
            "username": username,
            "password": password
        }
        text_msg = "{} {}:{}".format(plg.target, username, password)

    item = {
        "plg_name": getattr(plg, "_plugin_name", ""),
        "plg_type": plg.plugin_type,
        "vul_name": plg.vul_name,
        "app_name": plg.app_name,
        "target": plg.target,
        "verify_data": msg
    }

    if Conf.SAVE_JSON_RESULT_FILENAME:
        data = json.dumps(item)
        append_file(Conf.SAVE_JSON_RESULT_FILENAME, [data])

    if Conf.SAVE_TEXT_RESULT_FILENAME:
        data = str(msg)
        if text_msg:
            msg = text_msg

        if plg.plugin_type == PluginType.SNIFFER:
            pass

        elif plg.vul_name:
            if isinstance(msg, str) and "://" in msg:
                data = "{}----{}".format(plg.vul_name, msg)
            else:
                data = "{}----{}----{}".format(plg.vul_name, plg.target, msg)

        append_file(Conf.SAVE_TEXT_RESULT_FILENAME, [data])