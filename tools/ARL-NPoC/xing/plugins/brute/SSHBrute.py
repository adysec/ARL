from xing.core.ServiceBrutePlugin import ServiceBrutePlugin
from xing.core import PluginType, SchemeType


class Plugin(ServiceBrutePlugin):
    def __init__(self):
        super(Plugin, self).__init__()
        self.plugin_type = PluginType.BRUTE
        self.vul_name = "SSH 弱口令"
        self.app_name = 'ssh'
        self.scheme = [SchemeType.SSH]

        self.username_file = "username_ssh.txt"
        self.password_file = "password_ssh.txt"

    def service_brute(self):
        return self._crack_user_pass()




