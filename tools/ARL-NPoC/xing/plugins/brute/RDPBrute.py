from xing.core.ServiceBrutePlugin import ServiceBrutePlugin
from xing.core import PluginType, SchemeType



"""
Win 10 下有点问题
"""

class Plugin(ServiceBrutePlugin):
    def __init__(self):
        super(Plugin, self).__init__()
        self.plugin_type = PluginType.BRUTE
        self.vul_name = "RDP 弱口令"
        self.app_name = 'rdp'
        self.scheme = [SchemeType.RDP]

        self.username_file = "username_rdp.txt"
        self.password_file = "password_rdp.txt"

    def service_brute(self):
        return self._crack_user_pass()




