import http.server
import socketserver
from urllib.parse import urlparse
from urllib.parse import parse_qs
from sys import stderr

PORT = 8000


class serveRA(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text")
        self.end_headers()
        query = parse_qs(urlparse(self.path).query)
        if 'grpName' in query:
            grpName = query['grpName'][0]
            try:
                file = open(f"./wlgrps/{grpName}.cfg", 'rb')
            except:
                print('failed to open file!', file=stderr)
                return
            self.copyfile(file, self.wfile)
            file.close()
        return


def startServer():
    handler = serveRA

    with socketserver.TCPServer(("", PORT), handler) as httpd:
        print('starting server!')
        httpd.serve_forever()


startServer()
