from http.server import HTTPServer, SimpleHTTPRequestHandler
from pathlib import PurePath
from threading import local as t_local
from os.path import isdir, dirname
from subprocess import Popen, DEVNULL

import pkg_resources

# Thread local variable with .dir parameter specifying what dir the server should be on
local = t_local()

class CORSRequestHandler (SimpleHTTPRequestHandler):
    """
    Handler which adds CORS functionality to python's built in http.server
    and uses directory referenced by local.dir

    Args:
        SimpleHTTPRequestHandler (_type_): http.server handler to extend functionality on
    """
    def __init__(self, *args, **kwargs):
        super().__init__(directory=local.dir, *args, **kwargs)

    def end_headers (self):
        """
        Sends CORS line ending the MIME headers
        """
        self.send_header('Access-Control-Allow-Origin', '*')
        SimpleHTTPRequestHandler.end_headers(self)

    def do_OPTIONS(self):
        """
        Handles OPTION requests as SimpleHTTPRequestHandler is unable to by default
        """
        self.send_response(200, "ok")
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
    
    def log_message(self, format, *args):
        """
        NOTE - Overrides HTTPServer.log_message()

        Omit output such that jupyter notebooks won't be covered in request info

        Args:
            format (_type_): _description_
        """
        pass

def host_file(path:PurePath, port:int=0)->None:
    """
    Generates a web server to serve files. 

    NOTE - use this only to serve files
    NOTE - runs forever, call in separate thread to run concurrently

    Args:
        path (PurePath): _description_
        port (int, optional): _description_. Defaults to 0.
    """
    if not isdir(path):
        path = dirname(path)
    Popen(["python", pkg_resources.resource_filename(__name__, "apps/updog-render/updog/__main__.py"), "--cors", "-d", f"{path}", "-p", f"{port}"], stdout=DEVNULL, stderr=DEVNULL, )


def host_application(path:PurePath, port:int=0)->None:
    """
    Generates a web server to serve applications.

    NOTE - Use this only to host applications locally, use host_file to server files
    NOTE - runs forever, call in a separate thread to run concurrently.
    Args:
        path (Purepath): File path pointing to a .zarr file
        port (int): port number to plug server into (default is 0 which is 1st available socket found)
    """

    with HTTPServer(("", port), CORSRequestHandler) as httpd:
        # Set dir
        global local
        if isdir(path):
            local.dir = path
        else:
            local.dir = dirname(path)

        # Serve files
        httpd.serve_forever()