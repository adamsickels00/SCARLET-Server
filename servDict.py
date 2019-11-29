from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import logging

infoStored = {"Placeholder Key":"Placeholder Value"}

class Serv(BaseHTTPRequestHandler):


    def _set_response(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):

        global infoStored

        if self.path == '/':
            self.path = '/index.html'

        try:
            self.send_response(200)
        except:
            self.send_response(404)

        if self.path == '/index.html':
            self.end_headers()
            self.wfile.write(bytes(json.dumps(infoStored), 'utf-8'))
        else:

            try:
                requestedKey = self.path[1:]
                requestedVal = infoStored[requestedKey]
            except:
                requestedVal = "NO VALUE STORED"
            self.end_headers()
            self.wfile.write(bytes(json.dumps(requestedVal), 'utf-8'))

    def do_POST(self):

        global infoStored

        content_length = int(self.headers['Content-Length'])  # Gets the size of data
        self.post_data = self.rfile.read(content_length)  # Gets the data itself

        self._set_response()
        self.wfile.write("POST request for {}".format(self.path).encode('utf-8'))

        print(self.post_data.decode('ascii'))
        infoStored.update(json.loads(self.post_data.decode('ascii')))


httpd = HTTPServer(('', 8080), Serv)
httpd.serve_forever()
