import http.server
import os
import re
import socketserver
import traceback
from time import sleep
from urllib.parse import urlparse
from urllib.parse import parse_qs
from sys import stderr

import requests

PORT = 8000


class serveRA(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        query = parse_qs(urlparse(self.path).query)
        if 'grpName' in query:
            self.send_response(200)
            self.send_header("Content-type", "text")
            self.end_headers()
            grpName = query['grpName'][0]
            grpfile = "./"
            if os.path.exists(f"./wlgrps/{grpName}.cfg"):
                grpfile += f"wlgrps/{grpName}.cfg"
            elif os.path.exists(f"./extgrps/{grpName}.cfg"):
                grpfile += f"extgrps/{grpName}.cfg"
            else:
                print("could not find admins file!", file=stderr)
                return
            try:
                file = open(grpfile, 'rb')
                firstline = file.readline().decode('utf-8')
                file.seek(0)
                if firstline.startswith('remotelist='):
                    remote = firstline.split('=')[1].strip()
                    response = requests.get(remote, headers={'Accept': 'text/html,*/*'})
                    print(f"remote list came back with status code {response.status_code}")
                    if response.status_code == 200:
                        responsetext = response.text
                        config = file.read().decode('utf-8')
                        confgrps = re.findall(r"permissions/(.+)=(.+)", config, flags=re.M)
                        baseperm = re.findall(r"permissions=(.+)", config, flags=re.M)
                        responsetext = re.sub(r"Group=(.+):(.+)", fr'Group=\1:{baseperm[0]}', responsetext, flags=re.M)
                        for congrp in confgrps:
                            responsetext = re.sub(rf"^Group=({congrp[0]}):(.+)", rf"Group=\1:{congrp[1]}", responsetext, flags=re.M)
                        self.wfile.write(responsetext.encode('utf-8'))
                        backupfile = open(f"./wlgrps/backup-{grpName}.cfg", 'wb')
                        backupfile.write(responsetext.encode('utf-8'))
                        backupfile.close()
                    else:
                        backupfile = open(f"./wlgrps/backup-{grpName}.cfg", 'rb')
                        self.copyfile(backupfile, self.wfile)
                        backupfile.close()
                else:
                    self.copyfile(file, self.wfile)
                file.close()
            except:
                print('failed to serve file!', file=stderr)
                print(traceback.format_exc(), file=stderr)
        else:
            self.send_error(400, 'please specify the group to pull from', 'no grpName specified!')
        return


def startServer():
    handler = serveRA

    started = False
    while not started:
        try:
            with socketserver.TCPServer(("", PORT), handler) as httpd:
                print('starting server!')
                httpd.serve_forever()
                started = True
        except:
            print("server did not start trying again!")
            sleep(5)


startServer()
