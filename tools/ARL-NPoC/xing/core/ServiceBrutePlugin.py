from xing.core.BasePlugin import BasePlugin
from xing.utils import random_choices, exec_system, load_file, append_file
from xing.conf import Conf
from xing.core import SchemeType
import logging
import os
import re

class ServiceBrutePlugin(BasePlugin):
    def __init__(self):
        super(ServiceBrutePlugin, self).__init__()
        self.gen_user_file = None
        self.gen_pass_file = None
        self.delay_scheme = [SchemeType.SSH, SchemeType.RDP]

    def _gen_user_pass_file(self):
        user_list, pass_list = self.load_dict()
        self.logger.info("load auth pair {}".format(len(user_list)))
        random_str = random_choices(6)
        random_user_file = os.path.join(Conf.TEMP_DIR,  random_str + ".user.txt")
        random_pass_file = os.path.join(Conf.TEMP_DIR,  random_str + ".pass.txt")
        append_file(random_user_file, user_list)
        append_file(random_pass_file, pass_list)
        self.gen_user_file = random_user_file
        self.gen_pass_file = random_pass_file

        self.debug_lever = 0
        if Conf.LOGGER_LEVEL <= logging.DEBUG:
            self.debug_lever = 7

        self.max_connection_limit = 15
        self.connection_delay = 100
        self.timeout = 10*60*1000

        for scheme in self.delay_scheme:
            if scheme in self.scheme:
                self.connection_delay = 1500
                self.timeout = 20*60*1000
                continue

    def _crack_user_pass(self):
        self._gen_user_pass_file()
        random_out_file = os.path.join(Conf.TEMP_DIR, random_choices(6) + ".out.txt")
        cmd = [
            "ncrack",
            "-oN", "'{}'".format(random_out_file),
            "-f",
            "-d{}".format(self.debug_lever),
            "-v",
            "-g cl=1,CL={},at=1,cd={}ms,cr=5,to={}ms".format(self.max_connection_limit,
                                                             self.connection_delay,
                                                             self.timeout),
            "--pairwise",
            "-U '{}'".format(self.gen_user_file),
            "-P '{}'".format(self.gen_pass_file),
            self.target
        ]

        exec_system(cmd)

        lines = load_file(random_out_file)

        if os.path.exists(random_out_file):
            os.unlink(random_out_file)

        os.unlink(self.gen_pass_file)
        os.unlink(self.gen_user_file)

        for line in lines:
            if "credentials on" not in line:
                continue
            pattern = r"Discovered\s+credentials\s+on\s+([^\s]+)\s+'([^\']+)'\s+'([^\']+)'"
            matches = re.findall(pattern, line)
            if matches:
                item = {
                    "username": matches[0][1],
                    "password": matches[0][2]
                }
                return item




