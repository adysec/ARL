import datetime
import dnslib
from dnslib import *
from xing.core import PluginType
from xing.core.BasePlugin import BasePlugin
from xing.conf import Conf
import sqlite3


class Plugin(BasePlugin):
    def __init__(self):
        super(Plugin, self).__init__()
        self.plugin_type = PluginType.LISTENER
        self.app_name = 'DNS log listener'
        self.vul_name = 'DNS Logging Listener'

    def init_db(self):
        conn = sqlite3.connect(Conf.DNS_LOG_DB)
        cur = conn.cursor()
        db_exists = cur.execute(
            """SELECT name FROM sqlite_master WHERE type='table';""").fetchall()

        if len(db_exists) == 0:
            cur.execute('''CREATE TABLE RECORD(SOURCE VARCHAR(255),DOMAIN TEXT, TYPE VARCHAR(32), DATE TEXT);''')
            self.logger.info('Created table RECORD')

        else:
            table_exists = cur.execute(
                """SELECT name FROM sqlite_master WHERE type='table' AND Name='RECORD';""").fetchall()

            if len(table_exists) == 0:
                cur.execute('''CREATE TABLE RECORD(SOURCE VARCHAR(255),DOMAIN TEXT, TYPE VARCHAR(32), DATE TEXT;''')
                self.logger.info('Created table RECORD')


    def insert(self, data):
        conn = sqlite3.connect(Conf.DNS_LOG_DB)
        cur = conn.cursor()
        src = data['source']
        domain = data['domain']
        qtype = data['type']
        qtime = data['time']

        cur.execute(f'''INSERT INTO RECORD VALUES (?, ?, ?, ?)''', (src, domain, qtype, qtime))
        conn.commit()
        conn.close()

    def listen(self, host, port):
        if port == 99999:
            port = 53

        import socket
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.bind((host, port))

        except os.error:
            self.logger.error(f'Port {port} is already being used')
            exit()

        try:
            self.init_db()

        except Exception as e:
            self.logger.error(f'error initializing database: {str(e)}')
            exit()

        self.logger.info(f'Now listening on port {port} at {host}')
        while True:
            try:
                data, addr = s.recvfrom(8192)
                self.logger.debug('receive data')
                self.logger.debug(f'get connection from {addr[0]}')
                parsed = None
                try:
                    parsed = DNSRecord.parse(data)

                except dnslib.DNSError:
                    self.logger.error('Cannot parse as DNS request')

                if parsed:
                    for q in parsed.questions:
                        domain = str(q.qname)[:-1]
                        qtype = QTYPE.get(q.qtype)
                        self.logger.info(f'Get request from {addr[0]} for domain {domain}, type {qtype}')
                        answer = parsed.reply()
                        answer.add_answer(RR(domain, QTYPE.A, rdata=A("127.0.0.1"), ttl=60))
                        response = answer.pack()
                        s.sendto(response, addr)

                        cur_time = str(datetime.datetime.now())
                        rdata = {
                            'source': addr[0],
                            'domain': domain,
                            'type': qtype,
                            'time': cur_time
                        }

                        self.insert(rdata)

            except KeyboardInterrupt:
                self.logger.debug('keyboard interrupt, stop listener')
                exit()
