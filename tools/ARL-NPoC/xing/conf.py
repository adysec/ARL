import os
import logging
import tempfile
import yaml


class Conf(object):
    """运行配置类"""

    """源码目录"""
    PROJECT_DIRECTORY = os.path.abspath(os.path.dirname(__file__))

    """系统插件目录"""
    SYSTEM_PLUGINS_DIR = os.path.join(PROJECT_DIRECTORY, "plugins")

    """用户自定义目录"""
    USER_PLUGINS_DIR = None

    """代理地址"""
    PROXY_URL = None

    """TXT格式保存文件名"""
    SAVE_TEXT_RESULT_FILENAME = "npoc_result_txt.txt"

    """JSON格式保存文件名"""
    SAVE_JSON_RESULT_FILENAME = "npoc_result_json.txt"

    """DATABASE DIRECTORY"""
    SYSTEM_DATABASE_DIR = os.path.join(PROJECT_DIRECTORY, "database")

    """DNS LOG DB"""
    DNS_LOG_DB = os.path.join(SYSTEM_DATABASE_DIR, "db_log.db")

    DUMP_RESULT_REQ_FLAG = False

    """连接超时时间"""
    CONNECT_TIMEOUT = 5.1
    """读取超时时间"""
    READ_TIMEOUT = 10.1

    """日志等级"""
    LOGGER_LEVEL = logging.INFO

    SUCCESS_LEVEL = 51

    """临时目录"""
    TEMP_DIR = tempfile.gettempdir()

    """HTTP AUTH TOKEN"""
    HTTP_API_AUTH_TOKEN = ''

    """HTTP API TEST"""
    HTTP_API_AUTH_ENABLE = False

    """HTTP API HOST"""
    HTTP_API_HOST = '127.0.0.1'

    """HTTP API PORT"""
    HTTP_API_PORT = 8080

    """EXTERNAL BINARY DIRECTORY"""
    SYSTEM_BINARY_DIR = os.path.join(PROJECT_DIRECTORY, "external")

    """JNDI LISTENER PATH"""
    JNDI_LISTENER_PATH = os.path.join(SYSTEM_BINARY_DIR, "jndi_listener-1.0-SNAPSHOT-all.jar")

    """MARSHALSEC JAR PATH"""
    MARSHALSEC_PATH = os.path.join(SYSTEM_BINARY_DIR, "marshalsec-0.0.3-SNAPSHOT-all.jar")

    """RMI LISTEN PORT"""
    JNDI_RMI_PORT = 1097

    """RMI HOST, PUBLIC_IP """
    JNDI_HOST = '127.0.0.1'

    """RMI HTTP SERVER PORT"""
    JNDI_HTTP_PORT = 8000

    """RMI PAYLOAD"""
    RMI_PAYLOAD = {
        'antServlet': 'ant',
        'tomcat': '',
        'tomcatServlet': 'yay',
        'tomcatFilter': '',
        'springController': 'yay',
        'springInterceptor': ''
    }

    """JNDI LISTENER PAYLOAD INFO"""
    JNDI_PAYLOAD_INFO = """
    支持payload一览:                                                                                                      
        0类payload (通过HTTP服务器获取class文件，仅限于较低版本的Java，高版本无效):                                        
        tomcat0             - 通过获取当前线程的 tomcat 请求执行命令，有回显，非内存马                                     
        tomcatServlet0      - 通过向 tomcat 添加 servlet 执行命令，路径为yay，参数为cmd，内存马                            
        tomcatFilter0       - 通过向 tomcat 添加 filter 内存马, 参数为y4y                                                  
        antServlet0         - 通过向 tomcat 添加 servlet，需要蚁剑客户端利用，路径为ant，参数为cmd，内存马                 
        springController0   - 通过向 spring 添加 controller，路径为/yay，参数为cmd，内存马                                 
        springInterceptor0  - 通过向 Spring 添加 Interceptor 内存马, 参数为y4y
    
        1类payload (利用Java的ELProcessor绕过对外部URL请求的限制，不依赖HTTP服务器):
        tomcat1             - 通过获取当前线程的 tomcat 请求执行命令，有回显，非内存马
        tomcatServlet1      - 通过向 tomcat 添加 servlet执行命令，路径为/yay，参数为cmd，内存马
        tomcatFilter1       - 通过向 tomcat 添加 filter 内存马, 参数为y4y
        antServlet1         - 通过向 tomcat 添加 servlet，需要蚁剑客户端利用，路径为/ant，参数为cmd，内存马
        springController1   - 通过向 Spring 添加 controller 内存马, 路径为/yay，参数为cmd，内存马   
        springInterceptor1  - 通过向 Spring 添加 Interceptor 内存马, 参数为y4y
    
        通用payload (同样利用ELProcessor进行绕过，但不支持内存马和回显):
        general_<base64编码后的指令> (例: cmd=whoami， payload名=general_d2hvYW1p)
        NPoC中只需要提供"general"，不需要提供后面的base64编码后的指令
        如： -c 'touch /tmp/pwn.txt' -o payload_type=general 
    """

    """YAML配置文件路径"""
    CONFIG_YAML_PATH = "config.yml"

    """Reverse Shell Platform IP"""
    SHELL_PLATFORM_IP = "127.0.0.1"

    """Reverse Shell Platform Port"""
    SHELL_PLATFORM_PORT = 80

    """Supported Reverse Shell Plugins List"""
    SUPPORT_SHELL_PLUGINS_FILE = os.path.join(SYSTEM_BINARY_DIR, 'Usable_Reverse_Shell_Plugins.txt')


def load_yaml_config():
    if os.path.isfile(os.path.join(Conf.PROJECT_DIRECTORY, Conf.CONFIG_YAML_PATH)):
        filename = os.path.join(Conf.PROJECT_DIRECTORY, Conf.CONFIG_YAML_PATH)

    else:
        return {}

    f = open(filename, 'r', encoding='utf-8')
    config = yaml.safe_load(f)
    return config


yml_config = load_yaml_config()

if yml_config.get('jndi'):
    if yml_config['jndi'].get('host'):
        Conf.JNDI_HOST = yml_config['jndi']['host']

    if yml_config['jndi'].get('port'):
        Conf.JNDI_RMI_PORT = int(yml_config['jndi']['port'])

    if yml_config['jndi'].get('http-port'):
        Conf.JNDI_HTTP_PORT = int(yml_config['jndi']['http-port'])

if yml_config.get('http'):
    if yml_config['http'].get('host'):
        Conf.HTTP_API_HOST = yml_config['http']['host']

    if yml_config['http'].get('port'):
        Conf.HTTP_API_PORT = int(yml_config['http']['port'])

    if yml_config['http'].get('auth_token'):
        Conf.HTTP_API_AUTH_TOKEN = yml_config['http']['auth_token']

    if yml_config['http'].get('auth_enabled'):
        Conf.HTTP_API_AUTH_ENABLE = yml_config['http']['auth_enabled']


if yml_config.get("shell_manager"):
    if yml_config['shell_manager'].get('host'):
        Conf.SHELL_PLATFORM_IP = yml_config["shell_manager"]["host"]

    if yml_config['shell_manager'].get('port'):
        Conf.SHELL_PLATFORM_PORT = int(yml_config["shell_manager"]["port"])

