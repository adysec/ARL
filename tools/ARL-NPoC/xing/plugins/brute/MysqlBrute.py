import re
import hashlib
import struct
import time
from xing.core.BasePlugin import BasePlugin
from xing.core import PluginType, SchemeType


class Plugin(BasePlugin):
    def __init__(self):
        super(Plugin, self).__init__()
        self.plugin_type = PluginType.BRUTE
        self.vul_name = "MySQL 弱口令"
        self.app_name = 'mysql'
        self.scheme = [SchemeType.MYSQL]

        self.username_file = "username_mysql.txt"
        self.password_file = "password_mysql.txt"

    def login(self, target, user, passwd):
        user_bytes = user.encode(encoding="utf-8")
        passwd_bytes = passwd.encode(encoding="utf-8")
        client = self.conn_target()
        data = client.recv(254)

        plugin, scramble = get_scramble(data)
        if scramble == "":
            self.logger.info("not found scramble {}:{} {}".format(user, passwd, target))
            return False

        auth_data = get_auth_data(user_bytes, passwd_bytes, scramble, plugin)
        client.send(auth_data)
        time.sleep(0.1)
        result = client.recv(1024)
        client.close()

        self.logger.debug("recv <<< {}".format(result))
        if result == b"\x07\x00\x00\x02\x00\x00\x00\x02\x00\x00\x00":
            return True

    def check_app(self, target):
        client = self.conn_target()
        data = client.recv(256)
        client.close()
        self.logger.debug("recv <<< {}".format(data))
        pattern = rb'^.\x00\x00\x00.*?mysql|^.\x00\x00\x00\n|.*?MariaDB server'
        matches = re.findall(pattern, data)

        if not matches:
            self.logger.debug("recv <<< {}".format(data))
            return False

        plugin, scramble = get_scramble(data)

        if scramble == "":
            return False

        check = b'is not allowed to connect'
        if check in data:
            self.logger.debug("recv <<< {}".format(data))
            return False

        return True


'''
参考
https://github.com/y1ng1996/F-Scrack/blob/master/F-Scrack.py
'''

def get_hash(password, scramble):
    hash_stage1 = hashlib.sha1(password).digest()
    hash_stage2 = hashlib.sha1(hash_stage1).digest()
    to = hashlib.sha1(scramble + hash_stage2).digest()
    reply = [h1 ^ h3 for (h1, h3) in zip(hash_stage1, to)]
    hash_data = struct.pack('20B', *reply)

    return hash_data


def get_scramble(packet):
    scramble, plugin = '', ''
    try:
        tmp = packet[15:]
        m = re.findall(rb"\x00?([\x01-\x7F]{7,})\x00", tmp)
        if len(m) > 3: del m[0]
        scramble = m[0] + m[1]
    except:
        return '', ''
    try:
        plugin = m[2]
    except:
        pass
    return plugin, scramble


def get_auth_data(user, password, scramble, plugin):
    common_bytes = bytes.fromhex("85a23f0000000040080000000000000000000000000000000000000000000000")

    pass_hash = get_hash(password, scramble)

    if not password:
        data = common_bytes + user + bytes.fromhex("0000")
    else:
        data = common_bytes + user + bytes.fromhex("0014") + pass_hash

    if plugin:
        data += plugin
        data += bytes.fromhex("0055035f6f73076f737831302e380c5f636c69656e745f6e616d65086c69626d7973716c045f7069640539323330360f5f636c69656e745f76657273696f6e06352e362e3231095f706c6174666f726d067838365f3634")

    len_bytes = struct.pack('B', len(data))
    auth_data = len_bytes + bytes.fromhex("000001") + data

    return auth_data




