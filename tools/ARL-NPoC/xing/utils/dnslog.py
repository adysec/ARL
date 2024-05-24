import json
import time
from . import get_logger
from . import http_req

logger = get_logger()


def xn_9tr_com_get(raise_error=True):
    """
    从 https://log.xn--9tr.com 获取 domain 和 token
    return 为数组 (e.g. ["12345678.dns.1433.eu.org", "qkyyy8hjlblg"] )
    Get: https://log.xn--9tr.com/new_gen
    Api: https://log.xn--9tr.com/qkyyy8hjlblg
    """

    try:
        request = http_req("https://log.xn--9tr.com/new_gen")
        data = request.json()
        return data["domain"], data["token"]
    except Exception as e:
        if raise_error:
            raise e

        return None, None


def xn_9tr_com_verify(token=None, raise_error=True):
    """
    用于获取 dnslog 结果
    Api: https://log.xn--9tr.com/qkyyy8hjlblg
    return 为: request.content
    """
    try:
        time.sleep(0.5)
        request = http_req("https://log.xn--9tr.com/" + token)
        return request.text

    except Exception as e:
        if raise_error:
            raise e
        return ""