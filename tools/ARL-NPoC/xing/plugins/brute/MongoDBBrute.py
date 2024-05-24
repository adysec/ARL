from pymongo import MongoClient
from urllib.parse import quote_plus
from xing.core.ServiceBrutePlugin import ServiceBrutePlugin
from xing.core import PluginType, SchemeType


class Plugin(ServiceBrutePlugin):
    def __init__(self):
        super(Plugin, self).__init__()
        self.plugin_type = PluginType.BRUTE
        self.vul_name = "MongoDB 弱口令"
        self.app_name = 'mongodb'
        self.scheme = [SchemeType.MONGODB]

        self.username_file = "username_mongodb.txt"
        self.password_file = "password_mongodb.txt"

    def login(self, target, user, passwd):
        host = self.target_info["host"]
        port = self.target_info["port"]
        if port is None:
            port = 27017
        uri = "mongodb://{}:{}@{}:{}".format(quote_plus(user),
                                             quote_plus(passwd),
                                             host, port)

        try:
            conn = MongoClient(uri, connectTimeoutMS=5000,
                               serverSelectionTimeoutMS=5000)
            self.logger.info(conn.admin.command("ping"))
            self.logger.success("{} login success".format(uri))
            return True
        except Exception as e:
            self.logger.debug("{} {}".format(uri, e))

        return False

    def check_app(self, target):
        host = self.target_info["host"]
        port = self.target_info["port"]
        if port is None:
            port = 27017
        uri = "mongodb://{}:{}@{}:{}".format("not_user", "not_pass!23af",
                                             host, port)
        try:
            conn = MongoClient(uri, connectTimeoutMS=5000,
                               serverSelectionTimeoutMS=5000)
            self.logger.info(conn.test.command("ping"))
        except Exception as e:
            self.logger.debug("{} {}".format(uri, e))
            if 'Authentication failed' in str(e):
                return True

        return False


"""
创建容器
docker run -p 27018:27017 -it --rm -e MONGO_INITDB_ROOT_USERNAME=root -e MONGO_INITDB_ROOT_PASSWORD=secret mongo:4.0 mongod

"""






