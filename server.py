#! /bin/python3
from sympy import *
import sympy.plotting as plotting
import requests, zipfile, os
from http.server import HTTPServer, BaseHTTPRequestHandler
from socketserver import ThreadingMixIn

port = int(os.getenv("PORT", "80"))
ip = str(os.getenv("IP", "0.0.0.0"))

print("Preparing to print on {}".format((ip, port)))

def pull_req():
    #TODO
    r = requests.get("http://fontawesome.io/assets/font-awesome-4.7.0.zip")
    print(r.text)


#if __name__ == "__main__":
#   pull_req()

class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    """
    Stolen from https://stackoverflow.com/questions/14088294/multithreaded-web-server-in-python (THANKS BTW)
    """

class 

