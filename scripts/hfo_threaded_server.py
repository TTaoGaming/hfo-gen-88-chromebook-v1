# Medallion: Bronze | Mutation: 88% | HIVE: V
import http.server
import socketserver
import os
import sys

PORT = 8889

class ThreadedHTTPServer(socketserver.ThreadingMixIn, http.server.HTTPServer):
    daemon_threads = True

class MyHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        # Add CORS and Cache-Control for development stability
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate')
        super().end_headers()

if __name__ == "__main__":
    server_address = ('', PORT)
    httpd = ThreadedHTTPServer(server_address, MyHandler)
    print(f"🚀 [HFO SERVER]: Multi-threaded Armored Server started on port {PORT}")
    print(f"🏠 [BASE]: {os.getcwd()}")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n🛑 [HFO SERVER]: Shutting down.")
        httpd.server_close()
        sys.exit(0)
