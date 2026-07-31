import http.server
import ssl
import os
import socket
import subprocess

DIR = os.path.dirname(os.path.abspath(__file__))
os.chdir(DIR)

MKCERT = "/opt/homebrew/bin/mkcert"
CERT = os.path.join(DIR, "cert.pem")
KEY = os.path.join(DIR, "key.pem")


def current_lan_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))  # no packet actually sent; just picks the outbound interface
        return s.getsockname()[0]
    except Exception:
        return "127.0.0.1"
    finally:
        s.close()


def local_hostname():
    try:
        name = subprocess.run(
            ["/usr/sbin/scutil", "--get", "LocalHostName"],
            check=True, capture_output=True, text=True,
        ).stdout.strip()
        return name + ".local"
    except Exception:
        return None


def ensure_cert_for(ip, hostname):
    names = [ip, "localhost", "127.0.0.1"]
    if hostname:
        names.insert(0, hostname)
    subprocess.run([MKCERT, "-cert-file", CERT, "-key-file", KEY] + names, check=True, cwd=DIR)


ip = current_lan_ip()
hostname = local_hostname()
ensure_cert_for(ip, hostname)

server = http.server.HTTPServer(("0.0.0.0", 8443), http.server.SimpleHTTPRequestHandler)
ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
ctx.load_cert_chain(certfile=CERT, keyfile=KEY)
server.socket = ctx.wrap_socket(server.socket, server_side=True)

print("Serving HTTPS on 0.0.0.0:8443 (cert valid for " + ip + (", " + hostname if hostname else "") + ") from", DIR)
server.serve_forever()
