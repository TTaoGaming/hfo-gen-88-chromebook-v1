#!/usr/bin/env python3
import http.server
import socketserver
import os

# Medallion: Bronze | Mutation: 0% | HIVE: P
# P0-SERVER: Header-Compliant WASM Server for Rapier/MediaPipe

PORT = 8094
DIRECTORY = "/home/tommytai3/active/hfo_gen_88_chromebook_v_1/hfo_hot_obsidian/bronze/2_areas/mission_thread_omega"

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

    def end_headers(self):
        # Mandatory for multi-threaded WASM and Cross-Origin isolation
        self.send_header('Cross-Origin-Embedder-Policy', 'require-corp')
        self.send_header('Cross-Origin-Opener-Policy', 'same-origin')
        self.send_header('Access-Control-Allow-Origin', '*')
        super().end_headers()

    def do_GET(self):
        # Ensure WASM files are served with the correct MIME type
        if self.path.endswith('.wasm'):
            self.extensions_map.update({'.wasm': 'application/wasm'})
        return super().do_GET()

if __name__ == "__main__":
    os.chdir(DIRECTORY)
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print(f"🚀 P0-SERVER: Serving at http://localhost:{PORT}")
        print(f"📂 Directory: {DIRECTORY}")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nShutting down server.")
            httpd.shutdown()
