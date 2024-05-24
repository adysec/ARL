#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import socket
import sys
import time
from xing.utils.file import load_file, clear_empty
from requests.exceptions import ReadTimeout, ConnectionError, ConnectTimeout
from xing.core import ObjectDict, SubParser
from xing.core import init_args, PluginType, plugin_runner
from xing.utils import get_logger, load_plugins, pattern_match
from xing import utils
from xing.conf import Conf
from xing.core.ShellManager import ShellManager

settings = ObjectDict()

plugins = load_plugins(os.path.join(Conf.PROJECT_DIRECTORY, "plugins"))


def show_plugins(args):
    cnt = 0
    for plugin in plugins:
        plugin_name = plugin._plugin_name
        if pattern_match(args.plugin_name, plugin_name):
            cnt += 1

            if plugin.plugin_type == PluginType.SNIFFER:
                print("[{}][{}-{}] {} ".format(cnt,plugin.plugin_type,
                    plugin.target_scheme, plugin_name ))
            else:
                print("[{}][{}] {} | {}".format(cnt, plugin.plugin_type,
                plugin_name, plugin.vul_name))


def load_plugin_by_filter(plugin_type, filter_name):
    filter_plugins = []
    for plugin in plugins:
        plugin_name = plugin._plugin_name
        if plugin.plugin_type != plugin_type:
            continue
        
        if not pattern_match(filter_name, plugin_name):
            continue

        filter_plugins.append(plugin)

    return filter_plugins


def scan(args):
    logger = get_logger()
    filter_plugins = load_plugin_by_filter(PluginType.POC,
                                           args.plugin_name)

    logger.info("load plugin {} ".format(len(filter_plugins)))
    plugin_runner(plugins=filter_plugins,
                  targets=load_targets(args.target), concurrency=args.concurrency_count)


def sniffer(args):
    logger = get_logger()
    filter_plugins = load_plugin_by_filter(PluginType.SNIFFER,
                                           args.plugin_name)

    logger.info("load plugin {} ".format(len(filter_plugins)))
    plugin_runner(plugins=filter_plugins,
                  targets=load_targets(args.target), concurrency=args.concurrency_count)


def exploit(args):
    logger = get_logger()
    filter_plugins = load_plugin_by_filter(PluginType.POC,
                                           args.plugin_name)

    plg_list = []
    for plg in filter_plugins:
        if not getattr(plg, "exploit_cmd", None):
            continue
        plg_list.append(plg)

    logger.info("load plugin {} ".format(len(plg_list)))
    for plg in plg_list:
        utils.run_exploit_cmd(plg, args)


def shell(args):
    logger = get_logger()
    supported_plugins = clear_empty(load_file(Conf.SUPPORT_SHELL_PLUGINS_FILE))
    filter_plugins = load_plugin_by_filter(PluginType.POC,
                                           args.plugin_name)
    plg_list = []
    for plg in filter_plugins:
        if not getattr(plg, "exploit_cmd", None):
            continue

        if plg._plugin_name not in supported_plugins:
            logger.debug('This Plugin Is Not Supported For Reverse Shell')
            continue
        plg_list.append(plg)

    logger.info("load plugin {} ".format(len(plg_list)))

    check_sh = ShellManager()
    if not check_sh.check_service():
        logger.error('reverse shell platform unavailable')
        return

    def run_exploit(sh, plg, args):
        try:
            utils.run_exploit_cmd(plg, args)
        except ReadTimeout:
            logger.debug('ReadTimeOut')

        except socket.timeout:
            logger.debug('SocketTimeOut')

        except ConnectTimeout:
            logger.debug('ConnectTimeOut')

        except ConnectionError:
            logger.debug('ConnectionError')

        except Exception as e:
            logger.debug(f'Unexpected Error: {str(e)}')

        logger.info("time sleep 3, wait conn")
        time.sleep(3)

        status = sh.check_connection()
        if status == "Connected":
            logger.success("URL: {}".format(sh.conn_url))
            return True

        return False

    for plg in plg_list:
        sh = ShellManager()
        sh.check_port()
        sh.create_session()
        payload1 = sh.generate_payload1()
        args.cmd = payload1
        if not run_exploit(sh, plg, args):
            logger.info('Trying Payload2 For Reverse Shell')
            payload2 = sh.generate_payload2()
            args.cmd = payload2
            run_exploit(sh, plg, args)


def brute(args):
    logger = get_logger()
    username_file = args.username_file
    if username_file:
        username_file = os.path.abspath(username_file)
        if not os.path.isfile(username_file):
            logger.warning("not found user file {}".format(username_file))
            return

    password_file = args.password_file
    if password_file:
        password_file = os.path.abspath(password_file)
        if not os.path.isfile(password_file):
            logger.warning("not found  password_file {}".format(password_file))
            return

    filter_plugins = load_plugin_by_filter(PluginType.BRUTE, args.plugin_name)
    logger.info("load plugin {} ".format(len(filter_plugins)))
    for plg in filter_plugins:
        if username_file:
            plg.username_file = username_file
        if password_file:
            plg.password_file = password_file

    plugin_runner(plugins=filter_plugins,
                  targets=load_targets(args.target), concurrency=args.concurrency_count)


def listener(args):
    logger = get_logger()
    listener_plugins = load_plugin_by_filter(PluginType.LISTENER, args.plugin_name)
    logger.info(f"load listener with plugin name {args.plugin_name}")
    plg_list = []
    for plg in listener_plugins:
        if not getattr(plg, "listen", None):
            continue
        plg_list.append(plg)
        logger.info(f'loaded plugin: {plg.app_name}')
        utils.run_listener(plg, args)

    exit()


def load_targets(target):
    if os.path.isfile(target):
        return utils.load_file(target)
    else:
        return [target]


def main():
    args, parser = init_args()
    if args.subparser == SubParser.LIST:
        show_plugins(args)
        sys.exit()
    
    elif args.subparser == SubParser.SCAN:
        scan(args)
        sys.exit()

    elif args.subparser == SubParser.SNIFFER:
        sniffer(args)
        sys.exit()

    elif args.subparser == SubParser.EXPLOIT:
        exploit(args)
        sys.exit()

    elif args.subparser == SubParser.BRUTE:
        brute(args)
        sys.exit()

    elif args.subparser == SubParser.LISTENER:
        listener(args)
        sys.exit()

    elif args.subparser == SubParser.SHELL:
        # 不支持
        sys.exit()

    else:
        parser.print_usage()
        sys.exit()


if __name__ == '__main__':  # pragma: no cover
    main()

