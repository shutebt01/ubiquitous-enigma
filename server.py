#! /bin/python3
from sympy import *
import sympy.plotting as plotting
import requests, zipfile, os, os.path
from http.server import HTTPServer, BaseHTTPRequestHandler
from socketserver import ThreadingMixIn
from scss import parser
from urllib.parse import urlparse

debug=True

port = int(os.getenv("PORT", "80"))
ip = str(os.getenv("IP", "0.0.0.0"))

print("Preparing to print on {}".format((ip, port)))

def pullReq():
    #TODO
    r = requests.get("http://fontawesome.io/assets/font-awesome-4.7.0.zip")
    print(r.text)


#if __name__ == "__main__":
#   pullReq()

class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    """
    Stolen from https://stackoverflow.com/questions/14088294/multithreaded-web-server-in-python (THANKS BTW)
    """

locCache = dict()

def getLocation(name):
        global locCache
        # Intention is to flatten out structure, but to allow for file differentiation
        rootdir = name.split("/")[1]
        if rootdir in ["css", "dynamic", "lib", "static"]:
            # Direct pointer to file
            return name
        elif rootdir in locCache:
            # Cache Generated
            return locCache[rootdir] + name
        else:
            # TODO
            for i in os.listdir("css"):
                locCache[i] = "css"
            for i in os.listdir("dynamic"):
                locCache[i] = "dynamic"
            for i in os.listdir("lib"):
                locCache[i] = "lib"
            for i in os.listdir("static"):
                locCache[i] = "static"
            if rootdir in locCache:
                return locCache[rootdir] + name
            else:
                return None

def compileSCSS(filename):
    return parser.load(filename)

class IncomingHandler(BaseHTTPRequestHandler):

    def returnFile(self, filename, mime=None):
        if os.path.isfile(filename):
            self.send_response(200, "OK")
            if debug:
                self.send_header("Dev-Test", "File Path: {}".format(filename))
            if mime:
                self.send_header("Content-Type", mime)
            self.end_headers()
            with open(filename, "rb") as f:
                senddata = f.read()
                self.wfile.write(senddata)
        else:
            self.send_error(404, "Not File", "The file you requested was a directory")
            self.end_headers()

    def returnData(self, data, mime=None):
        self.send_response(200, "OK")
        if mime:
            print(mime)
            self.send_header("Content-Type", mime)
        self.end_headers()
        self.wfile.write(data.encode())

    def do_GET(self):
        url = urlparse(self.path)
        truePath = getLocation(url.path)
        if truePath.lower().endswith("scss"):
            css = compileSCSS(truePath)
            self.returnData(css, "text/css")
        else:
            self.returnFile(truePath)




if __name__ == "__main__":
    httpd = ThreadedHTTPServer((ip, port), IncomingHandler)
    httpd.serve_forever()