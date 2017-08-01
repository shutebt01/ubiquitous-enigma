#! /bin/python3
from sympy import *
import sympy.plotting as plotting
import requests, zipfile, os, os.path, json, urllib, urllib.parse, importlib, traceback
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
        rootdir = name.split("/")
        if len(rootdir) <= 1:
            return None
        rootdir = rootdir[1]
        if rootdir in ["css", "dynamic", "lib", "static", "js"]:
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
            for i in os.listdir("js"):
                locCache[i] = "js"
            for i in os.listdir("static"):
                locCache[i] = "static"
            if rootdir in locCache:
                return locCache[rootdir] + name
            else:
                return None

def compileSCSS(filename):
    p = parser.Stylesheet( options=dict( compress=True, cache=True ) )
    #return parser.load(filename)
    return p.load(filename)

class IncomingHandler(BaseHTTPRequestHandler):

    def returnFile(self, filename, mime=None, code=200):
        if os.path.isfile(filename):
            self.send_response(code, "OK")
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

    def returnData(self, data, mime=None, code=200):
        if not isinstance(data, bytes):
            data = data.encode()
        self.send_response(code, "OK")
        if mime:
            self.send_header("Content-Type", mime)
        self.end_headers()
        self.wfile.write(data)

    def handleDynamicCode(self):
        #get arguments
        arguments = dict()

        #From URL
        url = urlparse(self.path)
        qsplit = url.query.split("&")
        for i in qsplit:
            if "=" in i:
                spli = i.split("=")
                arguments[spli[0]] = spli[1]
            else:
                self.log_message("Unable to parse query param: %s", i)

        #From POST/PUT data:
        if self.command in ["PUT", "POST"]:
            if self.headers["Content-Type"] in ["text/json", "application/json"]:
                data = self.rfile.read(int(self.headers["Content-Length"]))
                data = data.decode()
                data = json.loads(data)
                arguments.update(data)

        #Decode any encoded arguments
        decode = dict()
        for key in arguments.keys():
            decode[urllib.parse.unquote(key)] = urllib.parse.unquote(arguments[key])
        arguments = decode

        #Call Func
        if "fun" in arguments:
            try:
                tgt = importlib.import_module("dynamic" + url.path[:-3].replace("/","."))
                importlib.reload(tgt)
                function = getattr(tgt, arguments["fun"])
                del arguments["fun"]
                response = function(**arguments)
                del function
                del tgt
                if isinstance(response, dict):
                    self.returnData(response["data"], mime=response["datatype"], code=(response["code"] if "code" in response else 200))
                else:
                    self.returnData(response[1], mime=response[0], code=(response[2] if len(response) >= 3 else 200))
            except Exception as e:
                traceback.print_exc()
                self.send_error(500, "Internal Server Error", "Internal server error")
                self.end_headers()
        else:
            self.send_error(400, "No Method provided", "No Method provided")
            self.end_headers()
        #print(url)

        pass

    def resolvePath(self):
        """
        Gets the path from the url, and returns the resolved full path

        Invalid path handling (READ: 404) is put in here
        """
        pass

    def processRequest(self):
        url = urlparse(self.path)
        tgtpath = url.path
        if tgtpath.endswith("/"):
            tgtpath += "index.html"
        truePath = getLocation(tgtpath)
        if truePath == None or any(x in truePath for x in ["__pycache__", ".gitkeep"]):
            # Return 404 Error
            self.returnFile(getLocation("/404.html"), code=404)
            return
        elif truePath.startswith("dynamic"):
            #literally just a check to ensure no unintentional Remote execution
            self.handleDynamicCode()
            return
        elif not os.path.isfile(truePath):
            truePath += "/index.html"
        if truePath.lower().endswith("scss"):
            if "nocompile" in url.query:
                self.returnFile(truePath, mime="text/x-scss")
            else:
                css = compileSCSS(truePath)
                self.returnData(css, "text/css")
        else:
            self.returnFile(truePath)

    def do_GET(self):
        #print(self.headers)
        self.processRequest()
        if DEBUG:
            if DEBUG_GC:
                gc.collect()
            if DEBUG_DUMP_MEM_USAGE:
                print('Memory usage: %s (kb)' % resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
            #pdb.set_trace()


    def do_POST(self):
        self.processRequest()
        if DEBUG:
            if DEBUG_GC:
                gc.collect()
            if DEBUG_DUMP_MEM_USAGE:
                print('Memory usage: %s (kb)' % resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)


if __name__ == "__main__":
    #DEBUGGING
    DEBUG = True
    if DEBUG:
        DEBUG_GC=True
        DEBUG_DUMP_MEM_USAGE=True
        import gc, resource, pdb

    httpd = ThreadedHTTPServer((ip, port), IncomingHandler)
    httpd.serve_forever()