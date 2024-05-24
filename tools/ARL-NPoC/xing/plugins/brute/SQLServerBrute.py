from xing.core.ServiceBrutePlugin import ServiceBrutePlugin
from xing.core import PluginType, SchemeType


class Plugin(ServiceBrutePlugin):
    def __init__(self):
        super(Plugin, self).__init__()
        self.plugin_type = PluginType.BRUTE
        self.vul_name = "SQLServer 弱口令"
        self.app_name = 'sqlserver'
        self.scheme = [SchemeType.SQLSERVER]

        self.username_file = "username_sqlserver.txt"
        self.password_file = "password_sqlserver.txt"

    def service_brute(self):
        return self._crack_user_pass()






