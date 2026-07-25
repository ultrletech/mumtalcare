# serve.py
# A drop-in replacement for `py -m http.server` that sets correct MIME types
# for .wasm and .mjs files, which ONNX Runtime Web and service workers need.

import http.server
import socketserver

PORT = 8000

class CorrectMimeTypeHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        # Service workers require this header to control the whole site scope.
        self.send_header('Service-Worker-Allowed', '/')
        super().end_headers()

    def guess_type(self, path):
        if path.endswith('.wasm'):
            return 'application/wasm'
        if path.endswith('.mjs'):
            return 'application/javascript'
        return super().guess_type(path)

with socketserver.TCPServer(("", PORT), CorrectMimeTypeHandler) as httpd:
    print(f"Serving at http://localhost:{PORT}")
    httpd.serve_forever()