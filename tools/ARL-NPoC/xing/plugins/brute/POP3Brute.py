from xing.core.ServiceBrutePlugin import ServiceBrutePlugin
from xing.core import PluginType, SchemeType


class Plugin(ServiceBrutePlugin):
    def __init__(self):
        super(Plugin, self).__init__()
        self.plugin_type = PluginType.BRUTE
        self.vul_name = "POP3 弱口令"
        self.app_name = 'POP3'
        self.scheme = [SchemeType.POP3]
        self.username_file = "username_pop3.txt"
        self.password_file = "password_pop3.txt"

    def service_brute(self):
        return self._crack_user_pass()
