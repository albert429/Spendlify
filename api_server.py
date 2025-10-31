import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs
from auth import login_user, register_user
from transactions import add_transaction, get_transactions, delete_transaction

HOST = "localhost"
PORT = 5000

class SimpleAPI(BaseHTTPRequestHandler):
    def _set_headers(self, code=200):
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, DELETE, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_POST(self):
        length = int(self.headers.get("Content-Length"))
        data = json.loads(self.rfile.read(length))

        if self.path == "/login":
            user = login_user(data["username"], data["password"])
            if user:
                self._set_headers(200)
                self.wfile.write(json.dumps(user).encode())
            else:
                self._set_headers(401)
                self.wfile.write(json.dumps({"error": "Invalid credentials"}).encode())

        elif self.path == "/register":
            result = register_user(data["username"], data["password"], data["full_name"], data["currency"])
            self._set_headers(200)
            self.wfile.write(json.dumps(result).encode())

        elif self.path == "/transactions/add":
            add_transaction(data)
            self._set_headers(200)
            self.wfile.write(json.dumps({"success": True}).encode())

    def do_GET(self):
        if self.path.startswith("/transactions"):
            username = self.path.split("?user=")[-1]
            txs = get_transactions(username)
            self._set_headers(200)
            self.wfile.write(json.dumps(txs).encode())

def run():
    print(f"Server running on http://{HOST}:{PORT}")
    HTTPServer((HOST, PORT), SimpleAPI).serve_forever()

if __name__ == "__main__":
    run()
