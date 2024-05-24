

class PluginType:
    POC = "poc"
    SNIFFER = "sniffer"
    BRUTE = "brute"
    LISTENER = "listener"
    SHELL = "shell"


class SchemeType:
    AJP = "ajp"
    DUBBO = "dubbo"
    IIOP = "iiop"
    JDWP = "jdwp"
    LDAP = "ldap"
    MEMCACHED = "memcached"
    MONGODB = "mongodb"
    MYSQL = "mysql"
    SQLSERVER = "mssql"
    POSTGRESQL = "psql"
    ZOOKEEPER = "zookeeper"
    RSYNC = "rsync"
    ORACLE = "oracle"
    REDIS = "redis"
    RMI = "rmi"
    SSH = "ssh"
    FTP = "ftp"
    IMAP = "imap"
    T3 = "t3"
    SMTP = "smtp"
    RDP = "rdp"
    POP3 = "pop3"
    ZMTP = "zmtp"
    HTTP = "http"
    HTTPS = "https"
    SOCKS4 = "socks4"
    SOCKS5 = "socks5"
    NFS = "nfs"
    PROXY_HTTPS = "proxy_https" #支持connect语法
    COBALT_STRIKE = 'csts'  # COBALT_STRIKE 团队服务器
    HRPC = 'hrpc' # Hadoop Yarn RPC


DEFAULT_PORT_SCHEME_LIST = [SchemeType.IMAP, SchemeType.LDAP,
                            SchemeType.NFS, SchemeType.POP3, SchemeType.SMTP]


class AppType:
    WEBLOGIC = "WebLogic"
    THINKPHP = "ThinkPHP"


class SubParser:
    LIST = "list"
    SCAN = "scan"
    SNIFFER = "sniffer"
    EXPLOIT = "exploit"
    BRUTE = "brute"
    LISTENER = "listener"
    SHELL = "shell"
