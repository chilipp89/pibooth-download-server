#!/usr/bin/env python3

import http.server
import socketserver
import random
import os
import socket
from shutil import make_archive
import pathlib
import platform
import re
from time import sleep

import qrcode
import threading
import netifaces


MacOS = "Darwin"
Linux = "Linux"
Windows = "Windows"
operating_system = platform.system()
message = """
╭──────────────────────────────────────────────────────────────────╮
│ This port is being used. Try another port.                       │
│ If you are very sure that this port is NOT in use,               │
│ then try running this script again because there is known issue  │
│ where an error is thrown even though the port is not being used. │
│ This will be fixed very soon.                                    │
│                                                                  │
│ - Developers of qr-filetrasfer                                   │
╰──────────────────────────────────────────────────────────────────╯
"""

def FileUploadServerHandlerClass(file_name, auth):
    class FileTransferServerHandler(http.server.SimpleHTTPRequestHandler):

        _file_name = file_name
        _auth = auth

        def do_AUTHHEAD(self):
            self.send_response(401)
            self.send_header('WWW-Authenticate', 'Basic realm=\"qr-filetransfer\"')
            self.send_header('Content-type', 'text/html')
            self.end_headers()

        def do_GET(self):
            if self._auth is not None:
                # The authorization output will contain the prefix Basic, we should add it for comparing.
                if self.headers.get('Authorization') != 'Basic ' + (self._auth.decode()):
                    self.do_AUTHHEAD()
                    return

            # the self.path will start by '/', we truncate it.
            request_path = self.path[1:]
            if request_path != self._file_name:
                # access denied
                self.send_response(403)
                self.send_header("Content-type", "text/html")
                self.end_headers()
            else:
                super().do_GET()
    return FileTransferServerHandler


def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    return s.getsockname()[0]


def get_local_ips_available():
    """Get a list of all local IPv4 addresses except localhost"""
    try:
        ips = []
        for iface in netifaces.interfaces():
            ips.extend([x["addr"] for x in netifaces.ifaddresses(iface).get(netifaces.AF_INET, []) if x and "addr" in x])

        localhost_ip = re.compile('^127.+$')
        return [x for x in sorted(ips) if not localhost_ip.match(x)]

    except ModuleNotFoundError:
        pass


def random_port():
    def is_port_in_use(port: int) -> bool:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            return s.connect_ex(('localhost', port)) == 0

    rnd_port = random.randint(1024, 65535)
    while is_port_in_use(rnd_port):
        rnd_port = random.randint(1024, 65535)
    return rnd_port


def get_qr_code(address):
    qr = qrcode.QRCode(version=1,
                       error_correction=qrcode.constants.ERROR_CORRECT_L,
                       box_size=10,
                       border=4,)
    qr.add_data(address)
    qr.make()

    return qr


def start_download_server(file_path, auth=None, duration=6000):
    """
    Keyword Arguments:
    file_path        -- String indicating the path to download the file to
    img_path         -- String path to export img
    auth             -- String indicating base64 encoded username:password
    """

    port = random_port()

    local_ip = get_local_ip()

    if not os.path.exists(file_path):
        print("No such file or directory")
        return

    # Variable to mark zip for deletion, if the user uses a folder as an argument
    delete_zip = None
    abs_path = os.path.normpath(os.path.abspath(file_path))
    file_dir = os.path.dirname(abs_path)
    file_path = os.path.basename(abs_path)

    # change to directory which contains file
    os.chdir(file_dir)

    # Checking if given file name or path is a directory
    if os.path.isdir(file_path):
        zip_name = pathlib.PurePosixPath(file_path).name

        # Zips the directory
        path_to_zip = make_archive(zip_name, "zip", file_path)
        file_path = os.path.basename(path_to_zip)
        delete_zip = file_path

    # Tweaking file_path to make a perfect url
    file_path = file_path.replace(" ", "%20")

    handler = FileUploadServerHandlerClass(file_path, auth)
    httpd = socketserver.TCPServer(("", port), handler)

    # This is the url to be encoded into the QR code
    address = "http://" + str(local_ip) + ":" + str(port) + "/" + file_path

    th = threading.Thread(target=server_thread, args=(httpd, delete_zip, duration))
    th.daemon = True
    th.start()

    return address


def server_thread(http_d, delete_zip, duration):
    th = threading.Thread(target=http_d.serve_forever)
    th.daemon = True
    th.start()

    i = 0
    while i < duration:
        i += 1
        sleep(1)
    if delete_zip is not None:
        os.remove(delete_zip)

    http_d.shutdown()


if __name__ == "__main__":
    EXAMPLE = r"README.md"
    available_duration = 20

    adre = start_download_server(
            EXAMPLE,
            duration=available_duration
        )
    print(adre)
    sleep(available_duration)
    print("Server Shutdown")
    sleep(available_duration)
