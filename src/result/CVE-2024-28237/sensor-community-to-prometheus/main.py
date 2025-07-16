import os
import socketserver
import traceback
import http.server
from urllib.parse import urlsplit
import re

import metrics

sensors = re.split(r'\s*,\s*', os.getenv('SENSORS', ''))
sensors = [s for s in sensors if s]
assert sensors, 'env var SENSORS is empty, e.g.: "esp8266-1234567, esp8266-12345678, esp8266-1234567"'
print('running on port 8080, providing metrics for sensors:', sensors)

class HttpHandler(http.server.BaseHTTPRequestHandler):
    protocol_version = 'HTTP/1.1'

    def send(self, content: str, code: int, mime: str):
        content = content.encode('utf8')
        self.send_response(code)
        self.send_header('Content-Type', mime)
        self.send_header('Content-Length', str(len(content)))
        self.end_headers()
        self.wfile.write(content)

    def do_GET(self):
        try:
            url = urlsplit(self.path.strip() or '/')
            if url.path == '/metrics':
                return self.send(metrics.generate(sensors), code=200, mime='text/plain; version=0.0.4')
            return self.send('404 not found', code=404, mime='text/plain')
        except Exception as e:
            traceback.print_exc()
            return self.send(str(e), code=500, mime='text/plain')


class HttpServer(socketserver.ThreadingMixIn, http.server.HTTPServer):
    allow_reuse_address = True


server = HttpServer(('', 8080), HttpHandler)
server.serve_forever()
