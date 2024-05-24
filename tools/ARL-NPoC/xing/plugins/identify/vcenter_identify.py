from xing.core.BasePlugin import BasePlugin
from xing.utils import http_req, get_logger
from xing.core import PluginType, SchemeType
import re


class Plugin(BasePlugin):

    def __init__(self):
        super(Plugin, self).__init__()      
        self.plugin_type = PluginType.POC
        self.vul_name = "发现VMware vCenter"
        self.app_name = 'vCenter'
        self.scheme = [SchemeType.HTTP, SchemeType.HTTPS]


    def verify(self, target):

        xml = b"""
        <env:Envelope xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:env="http://schemas.xmlsoap.org/soap/envelope/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
            <env:Body>
                <RetrieveServiceContent xmlns="urn:vim25">
                    <_this type="ServiceInstance">ServiceInstance</_this>
                </RetrieveServiceContent>
            </env:Body>
        </env:Envelope>
        """
        url = f'{target}/sdk'
        req = http_req(url, method='post', data=xml)
        sc = req.status_code

        if sc == 200:
            resp = req.content
            fullname = re.findall(b'<fullName>(.*?)</fullName>', resp)
            if len(fullname) == 1:
                result = fullname[0].decode()
                self.logger.success("found vCenter {} at {}".format(result, url))
                return result
