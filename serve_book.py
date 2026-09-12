#!/usr/bin/env python3
import http.server, socketserver, os
os.chdir(os.path.join(os.path.dirname(__file__), "docs"))
PORT = int(os.environ.get("PORT", "8080"))
class H(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header("Cache-Control", "no-store")
        super().end_headers()
    def log_message(self, *a):
        print(*a)
with socketserver.TCPServer(("0.0.0.0", PORT), H) as httpd:
    print(f"BOOK http://0.0.0.0:{PORT}/", flush=True)
    httpd.serve_forever()
