import subprocess
import time
import json
import shlex
import random
import string
import urllib.parse
import inspect
import colorlog
import logging
import urllib3
import importlib
import os
from base64 import b64encode
import re
import sys
from urllib.parse import urlparse, urlsplit
from requests.models import PreparedRequest
urllib3.disable_warnings()
import requests
import hashlib
from xing.utils.file import load_file,append_file
from xing.conf import Conf


def exec_system(cmd, **kwargs):
    logger = get_logger()

    cmd = " ".join(cmd)
    logger.debug("exec system : {}".format(cmd))
    if "timeout" not in kwargs:
        kwargs["timeout"] = 4 * 60 * 60

    stdout = subprocess.DEVNULL
    stderr = subprocess.DEVNULL

    if Conf.LOGGER_LEVEL <= logging.DEBUG:
        stdout = None
        stderr = None

    completed = subprocess.run(shlex.split(cmd), stdout=stdout,stderr=stderr, check=False, **kwargs)

    return completed


def random_choices(k = 6):
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=k))




SUCCESS = Conf.SUCCESS_LEVEL
logging.addLevelName(SUCCESS, "SUCCESS")
def success(self, message, *args, **kws):
    if self.isEnabledFor(SUCCESS):
        self._log(SUCCESS, message, args, **kws) 
logging.Logger.success = success
 
def init_logger():
    log_colors = {
        'DEBUG': 'white',
        'INFO': 'green',
        'SUCCESS':  'red',
        'WARNING': 'yellow',
        'ERROR': 'red',
        'CRITICAL': 'bold_red',
    }

    handler = colorlog.StreamHandler()
    handler.setFormatter(colorlog.ColoredFormatter(
        fmt = '%(log_color)s[%(asctime)s] [%(levelname)s] '
              '[%(threadName)s] [%(filename)s:%(lineno)d] %(message)s', 
        log_colors = log_colors, datefmt = "%Y-%m-%d %H:%M:%S"))

    logger = colorlog.getLogger('xing')
    logger.setLevel(Conf.LOGGER_LEVEL)
    logger.addHandler(handler)
    logger.propagate = False


def get_celery_logger():
    try:
        from celery.utils.log import get_task_logger
        if 'celery' in sys.argv[0]:
            task_logger = get_task_logger(__name__)
            return task_logger
    except Exception as e:
        pass

    return None


def get_logger():
    task_logger = get_celery_logger()
    if task_logger is not None:
        return task_logger

    logger = logging.getLogger('xing')
    if not logger.handlers:
        init_logger()

    logger.setLevel(Conf.LOGGER_LEVEL)
    return logger


UA = "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36"


# http 请求封装函数
def http_req(url, method='get', **kwargs):
    if kwargs.get("disable_normal"):
        # 禁用 URL 规范化处理，仅仅支持GET
        kwargs.pop("disable_normal")
        return req_disable_normal(url, method, **kwargs)

    kwargs.setdefault('verify', False)
    kwargs.setdefault('timeout', (Conf.CONNECT_TIMEOUT, Conf.READ_TIMEOUT))
    kwargs.setdefault('allow_redirects', False)

    headers = kwargs.get("headers", {})
    if headers is None:
        headers = {}

    headers.setdefault("User-Agent", UA)

    random_ip = "10.0.{}.{}".format(random.randint(1, 254), random.randint(1, 254))
    headers.setdefault("X-Real-IP", random_ip)
    headers.setdefault("X-Forwarded-For", random_ip)

    kwargs["headers"] = headers

    proxies = {
        'https': Conf.PROXY_URL,
        'http': Conf.PROXY_URL
    }

    if Conf.PROXY_URL:
        kwargs["proxies"] = proxies

    conn = getattr(requests, method)(url, **kwargs)

    return conn


class MyPreparedRequest(PreparedRequest):
    def __init__(self):
        super().__init__()

    @property
    def path_url(self):
        url = []

        p = urlsplit(self.url, allow_fragments=False)

        path = p.path
        if not path:
            path = '/'

        url.append(path)

        query = p.query
        if query:
            url.append('?')
            url.append(query)

        return ''.join(url)


# 禁用规范化URL处理
# 下面这个函数在开代理的情况下依然是没有用的
def req_disable_normal(url, method='get', **kwargs):
    headers = kwargs.get("headers", {})
    if headers is None:
        headers = {}

    headers.setdefault("User-Agent", UA)

    kwargs["headers"] = headers

    req = requests.Request(method=method, url=url, **kwargs)
    prep = req.prepare()
    prep.url = url

    proxies = {}

    if Conf.PROXY_URL:
        proxies = {
            'http': Conf.PROXY_URL,
            'https': Conf.PROXY_URL
        }

    if "#" in url:
        my_prep = MyPreparedRequest()
        my_prep.prepare(method='GET', url=url)
        my_prep.url = url
        prep = my_prep

    with requests.Session() as session:
        return session.send(prep, verify=False, proxies=proxies, allow_redirects=False,
                            timeout=(Conf.CONNECT_TIMEOUT, Conf.READ_TIMEOUT))


def md5(data):
    hash_md5 = hashlib.md5()
    hash_md5.update(data.encode(encoding='utf-8'))
    return hash_md5.hexdigest()


def content2text(context, encoding="utf-8"):
    if isinstance(context, bytes):
        return context.decode(encoding, errors='ignore')

    return context


def parse_target_info(target):
    target = target.strip("/")

    if "://" not in target:
        target = "http://" + target

    parse = urlparse(target)
    
    port = parse.port

    if not parse.port:
        if parse.scheme == 'http':
            port = 80
        if parse.scheme == 'https':
            port = 443

    item = {
        'target':  target,
        'host': parse.hostname,
        'port': port,
        'scheme': parse.scheme
    }

    return item


def get_title(body):
    """
    根据页面源码返回标题
    :param body: <title>sss</title>
    :return: sss
    """
    result = ''
    title_patten = re.compile(rb'<title>([^<]{1,200})</title>', re.I)
    title = title_patten.findall(body)
    if len(title) > 0:
        try:
            result = title[0].decode("utf-8")
        except Exception as e:
            result = title[0].decode("gbk", errors="replace")
    return result.strip()


def run_exploit_cmd(plg, args):
    logger = get_logger()

    plg.set_target(args.target)
    _ = plg.target_info

    optional_args = dict(urllib.parse.parse_qsl(args.option))
    # 从配置文件读取 JNDI 平台信息
    optional_args.setdefault("remote", "{}:{}".format(Conf.JNDI_HOST, Conf.JNDI_RMI_PORT))
    optional_args.setdefault("payload_type", "general")
    optional_args.setdefault("key", "default")
    optional_args.setdefault("alg", "default")
    if plg.interact:
        rmi_payload_key = optional_args["payload_type"].strip("01")
        if rmi_payload_key not in Conf.RMI_PAYLOAD.keys() and optional_args["payload_type"] != "general":
            logger.warning("指定 payload {} 不存在".format(optional_args["payload_type"]))
            logger.warning(Conf.JNDI_PAYLOAD_INFO)

        if optional_args["payload_type"] == "general":
            optional_args["payload_type"] += "_" + b64encode(args.cmd.encode()).decode()

    exploit_args = inspect.getfullargspec(plg.exploit_cmd).args
    reserve_args = ['self', 'target', 'cmd']
    for key in reserve_args:
        if key in exploit_args:
            exploit_args.remove(key)

    lack_args = set(exploit_args) - set(optional_args.keys())

    if lack_args:
        info = '=value&'.join(lack_args)
        info += "=value"
        logger.info("额外参数: {}".format(optional_args))
        logger.info("{} 缺少参数：{}，请使用-o {} 提供".format(plg._plugin_name, " ".join(lack_args), info))
        return

    run_args = dict()
    for arg in exploit_args:
        run_args[arg] = optional_args[arg]

    logger.debug("target: {}, execute cmd: {}".format(plg.target, args.cmd))
    plg.exploit_cmd(target=plg.target, cmd=args.cmd, **run_args)


def run_listener(plg, args):
    logger = get_logger()

    optional_args = dict(urllib.parse.parse_qsl(args.option))
    listener_args = inspect.getfullargspec(plg.listen).args
    reserve_args = ['self', 'host', 'port']
    for key in reserve_args:
        if key in listener_args:
            listener_args.remove(key)

    if "JNDI" in plg.app_name:
        optional_args.setdefault("hostname", None)
        optional_args.setdefault("nolog", False)

    lack_args = set(listener_args) - set(optional_args.keys())
    if lack_args:
        info = '=value&'.join(lack_args)
        info += "=value"
        logger.info("额外参数: {}".format(optional_args))
        logger.info("{} 缺少参数：{}，请使用-o {} 提供".format(plg._plugin_name, " ".join(lack_args), info))
        return

    run_args = dict()
    for arg in listener_args:
        run_args[arg] = optional_args[arg]

    logger.info(f'loaded plugin: {plg.app_name}')
    plg.listen(args.host, args.port, **run_args)





from xing.utils.loader import load_all_plugin, load_plugins
from xing.utils.filter import pattern_match
from xing.utils.dnslog import xn_9tr_com_get, xn_9tr_com_verify
