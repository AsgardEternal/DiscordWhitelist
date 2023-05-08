import http.server
import os
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
            grpfile = "./"
            if os.path.exists(f"./wlgrps/{grpName}.cfg"):
                grpfile += f"wlgrps/{grpName}.cfg"
            elif os.path.exists(f"./extgrps/{grpName}.cfg"):
                grpfile += f"extgrps/{grpName}.cfg"
            else:
                print("could not find admins file!", file=stderr)
            try:
                file = open(grpfile, 'rb')
                self.copyfile(file, self.wfile)
                file.close()
            except:
                print('failed to open file!', file=stderr)
        return


def startServer():
    handler = serveRA

    with socketserver.TCPServer(("", PORT), handler) as httpd:
        print('starting server!')
        httpd.serve_forever()


startServer()
