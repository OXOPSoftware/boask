# boask/core.py
import http.server
import socketserver
import urllib.parse
import os

ROUTES = {}
MIDDLEWARES = []
PORT = 8080
STATIC_DIR = "static"

def route(path: str):
    def decorator(func):
        ROUTES[path] = func
        return func
    return decorator

def use(middleware_func):
    MIDDLEWARES.append(middleware_func)

class BoaskHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path

        for mw in MIDDLEWARES:
            mw(self)

        if path.startswith("/static/"):
            file_path = os.path.join(STATIC_DIR, path[8:].lstrip("/"))
            full_path = os.path.abspath(file_path)
            if full_path.startswith(os.path.abspath(STATIC_DIR)) and os.path.isfile(full_path):
                return super().do_GET()
            else:
                self.send_error(404, "File not found")
                return

        if path in ROUTES:
            try:
                response = ROUTES[path](self)
                if isinstance(response, str):
                    response = response.encode("utf-8")
                elif not isinstance(response, bytes):
                    response = b""
                self.send_response(200)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.send_header("Content-Length", str(len(response)))
                self.end_headers()
                self.wfile.write(response)
            except Exception as e:
                self.send_error(500, f"Boask Error: {str(e)}")
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"<h1>Boask: 404 - Not Found</h1>")

def run_server(port: int = 8080, host: str = ""):
    global PORT
    PORT = port
    os.makedirs(STATIC_DIR, exist_ok=True)
    
    print(f"Boask is running → http://localhost:{port}")
    print(f"Static: ./{STATIC_DIR}/")
    print(f"Templates: ./templates/")
    
    with socketserver.TCPServer((host, port), BoaskHandler) as server:
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            print("\nBoask stopped.")