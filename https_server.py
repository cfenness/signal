import http.server
import ssl
import os

DIR = os.path.dirname(os.path.abspath(__file__))
os.chdir(DIR)

CERT = os.path.join(DIR, "192.168.68.58+2.pem")
KEY = os.path.join(DIR, "192.168.68.58+2-key.pem")

server = http.server.HTTPServer(("0.0.0.0", 8443), http.server.SimpleHTTPRequestHandler)
ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
ctx.load_cert_chain(certfile=CERT, keyfile=KEY)
server.socket = ctx.wrap_socket(server.socket, server_side=True)

print("Serving HTTPS on 0.0.0.0:8443 from", DIR)
server.serve_forever()
