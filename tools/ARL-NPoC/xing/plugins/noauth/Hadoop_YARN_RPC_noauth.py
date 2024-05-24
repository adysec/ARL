import time
from xing.core.BasePlugin import BasePlugin
import base64
from xing.core import PluginType, SchemeType


class Plugin(BasePlugin):
    def __init__(self):
        super(Plugin, self).__init__()
        self.plugin_type = PluginType.POC
        self.vul_name = "Hadoop YARN RCP 未授权访问漏洞"
        self.scheme = [SchemeType.HRPC]

    def verify(self, target):
        base64_data = 'aHJwYwkAAAAAAF8aCAIQABgFIhArOwdm0CFF2Ym70jxlutaBKAFDEgkKB2ZyZWVtYW4aNm9yZy5hcGFjaGUuaGFkb29wLnlhcm4uYXBpLkFwcGxpY2F0aW9uQ2xpZW50UHJvdG9jb2xQQgAAAGgaCAIQABgAIhArOwdm0CFF2Ym70jxlutaBKABLCg9nZXRBcHBsaWNhdGlvbnMSNm9yZy5hcGFjaGUuaGFkb29wLnlhcm4uYXBpLkFwcGxpY2F0aW9uQ2xpZW50UHJvdG9jb2xQQhgBAA=='
        ack_data = base64.b64decode(base64_data)
        check = b"+;\x07f\xd0!E"
        client = self.conn_target()

        client.send(ack_data)
        time.sleep(0.2)
        data = client.recv(256)

        if b'Exception*' in data:
            return

        if data.startswith(b'\x00\x00') and check in data:
            self.logger.success("found {} {}".format(self.vul_name, target))
            return target
