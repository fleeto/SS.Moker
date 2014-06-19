# !/usr/bin/python
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import dataloader

PORT_NUMBER = 18080


class MockHandler(BaseHTTPRequestHandler):
    """
    This class will handles any incoming request from the browser
    """

    def do_GET(self):
        self.process_request('GET')
        return

    def do_POST(self):
        self.process_request('POST')
        return

    def process_request(self, method):
        """
        :param method:
        :return:
        """
        print self.path
        code, content, service = dataloader.get_data(method, self.path)
        self.send_response(code)
        if 'header' in service['response']:
            header = service['response']['header']
            for (key, value) in header.items():
                self.send_header(key, value)
        self.end_headers()
        # Send the html message
        self.wfile.write(content)
        return

try:

    server = HTTPServer(('', PORT_NUMBER), MockHandler)
    print 'Starting http server on port ', PORT_NUMBER

    #Wait forever for incoming http requests
    server.serve_forever()

except KeyboardInterrupt:
    print '^C received, shutting down the web server'
    server.socket.close()