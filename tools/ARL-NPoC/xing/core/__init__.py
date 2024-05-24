import argparse
import os
import logging
import importlib
import xing
from xing.conf import Conf


class ObjectDict(dict):
    """Makes a dictionary behave like an object, with attribute-style access.
    """

    def __getattr__(self, name):
        # type: (str) -> any
        try:
            return self[name]
        except KeyError:
            raise AttributeError(name)

    def __setattr__(self, name, value):
        # type: (str, any) -> None
        self[name] = value


class ArgumentDefaultsHelpFormatter(argparse.HelpFormatter):
    """Help message formatter which adds default values to argument help.

    Only the name of this class is considered a public API. All the methods
    provided by the class are considered an implementation detail.
    """

    def _get_help_string(self, action):
        help = action.help
        if '%(default)' not in action.help:
            if action.default is not argparse.SUPPRESS:
                defaulting_nargs = [argparse.OPTIONAL, argparse.ZERO_OR_MORE]
                if action.option_strings or action.nargs in defaulting_nargs:
                    if action.default is not None:
                        help += ' (default: %(default)s)'
        return help


def init_args():
    parser = argparse.ArgumentParser(prog="xing",
                                     formatter_class=ArgumentDefaultsHelpFormatter)

    parser.add_argument('--version', '-V',
                        action='version', version='%(prog)s ' + xing.__version__)

    parser.add_argument('--quit',
                        '-q',
                        action='store_true',
                        help='安静模式',
                        default=False)

    parser.add_argument('--log',
                        '-L',
                        default='info',
                        choices=["debug", "info", "success", "warning", "error"],
                        help='日志等级')

    subparsers = parser.add_subparsers(dest='subparser', help='子命令')
    parser_list = subparsers.add_parser(SubParser.LIST, help='显示插件')
    parser_list.add_argument('--pid', help='插件id')

    parser_list.add_argument('--app-name',
                             help='WEB应用名称名字')

    parser_list.add_argument('--plugin-name',
                             '-n',
                             default='*',
                             help='插件名称')

    parser_list.add_argument('--plugin-type',
                             '-t',
                             default='*',
                             choices=['poc', 'sniffer', 'listener'],
                             help='插件类别')

    parser_scan = subparsers.add_parser(SubParser.SCAN, help='扫描')
    parser_scan.add_argument('--target',
                             '-t',
                             help='目标文件或者URL',
                             required=True)

    parser_scan.add_argument('--concurrency-count',
                             '-c',
                             default=10,
                             type=int,
                             help='并发请求数量')

    parser_scan.add_argument('--pid', help='插件id')

    parser_scan.add_argument('--app-name',
                             help='WEB应用名称名字')

    parser_scan.add_argument('--plugin-name',
                             '-n',
                             default='*',
                             help='插件名称')

    parser_scan.add_argument('--proxy',
                             '-x',
                             help='代理地址')

    parser_sniffer = subparsers.add_parser(SubParser.SNIFFER, help='协议识别')
    parser_sniffer.add_argument('--target',
                                '-t',
                                help='目标文件或者URL',
                                required=True)

    parser_sniffer.add_argument('--concurrency-count',
                                '-c',
                                default=10,
                                type=int,
                                help='并发请求数量')

    parser_sniffer.add_argument('--plugin-name',
                                '-n',
                                default='*',
                                help='插件名称')

    parser_exploit = subparsers.add_parser(SubParser.EXPLOIT, help='漏洞利用')
    parser_exploit.add_argument('--target',
                                '-t',
                                help='目标文件或者URL',
                                required=True)

    parser_exploit.add_argument('--plugin-name',
                                '-n',
                                default='*',
                                help='插件名称')

    parser_exploit.add_argument('--cmd',
                                '-c',
                                required=True,
                                help='需要执行的命令')

    parser_exploit.add_argument('--proxy',
                                '-x',
                                help='代理地址')

    parser_exploit.add_argument('--option',
                                '-o',
                                required=False,
                                help='额外参数, 按照HTTP GET参数传递方式')

    parser_brute = subparsers.add_parser(SubParser.BRUTE, help='弱口令爆破')
    parser_brute.add_argument('--target',
                              '-t',
                              help='目标文件或者URL',
                              required=True)

    parser_brute.add_argument('--plugin-name',
                              '-n',
                              default='*',
                              help='插件名称')

    parser_brute.add_argument('--username-file',
                              '-U',
                              help='用户名文件')

    parser_brute.add_argument('--password-file',
                              '-P',
                              help='密码文件')

    parser_brute.add_argument('--proxy',
                              '-x',
                              help='代理地址')

    parser_brute.add_argument('--concurrency-count',
                              '-c',
                              default=6,
                              type=int,
                              help='并发请求数量')

    parser_listener = subparsers.add_parser(SubParser.LISTENER, help='监听')
    parser_listener.add_argument('--plugin-name',
                                 '-n',
                                 default='*',
                                 help='插件名称')

    parser_listener.add_argument('--host',
                                 '-H',
                                 default='127.0.0.1',
                                 help='监听地址')

    parser_listener.add_argument('--port',
                                 '-P',
                                 default=99999,
                                 type=int,
                                 help='监听端口')

    parser_listener.add_argument('--option',
                                 '-o',
                                 required=False,
                                 help='额外参数, 按照HTTP GET参数传递方式')

    parser_shell = subparsers.add_parser(SubParser.SHELL, help='反弹Shell')
    parser_shell.add_argument('--target',
                              '-t',
                              help='目标文件或者URL',
                              required=True)

    parser_shell.add_argument('--plugin-name',
                              '-n',
                              default='*',
                              help='插件名称')

    parser_shell.add_argument('--proxy',
                              '-x',
                              help='代理地址')

    parser_shell.add_argument('--option',
                              '-o',
                              required=False,
                              help='额外参数, 按照HTTP GET参数传递方式')

    args = parser.parse_args()

    update_conf(args)

    return args, parser


def update_conf(args):
    proxy = getattr(args, "proxy", None)
    if proxy:
        Conf.PROXY_URL = proxy

    loglevel = args.log
    numeric_level = getattr(logging, loglevel.upper(), None)
    if loglevel == "success":
        numeric_level = Conf.SUCCESS_LEVEL

    if not isinstance(numeric_level, int):
        raise ValueError('Invalid log level:{0}'.format(loglevel))

    Conf.LOGGER_LEVEL = numeric_level

    if args.quit:
        Conf.LOGGER_LEVEL = 1000


from xing.core.const import PluginType, SchemeType, AppType, DEFAULT_PORT_SCHEME_LIST, SubParser
from xing.core.PluginRunner import plugin_runner
from xing.core.BruteRunner import brute_runner
from xing.core.ThreadMap import thread_map
