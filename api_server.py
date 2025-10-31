import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs
from auth import login_user, register_user
from data_handler import load_transactions
from transactions import add_transaction, delete_transaction, get_user_transactions

HOST = "localhost"
PORT = 5000

class SimpleAPI(BaseHTTPRequestHandler):
    def _set_headers(self, code=200):
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()

    def _send_json(self, data, code=200):
        self._set_headers(code)
        self.wfile.write(json.dumps(data).encode())

    def _handle_error(self, error_msg, code=400):
        self._send_json({"error": error_msg}, code)

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, DELETE, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_POST(self):
        try:
            length = int(self.headers.get("Content-Length", 0))
            data = json.loads(self.rfile.read(length)) if length > 0 else {}

            if self.path == "/login":
                if "username" not in data or "password" not in data:
                    return self._handle_error("Missing username or password", 400)
                
                user = login_user(data["username"], data["password"])
                if user:
                    self._send_json(user)
                else:
                    self._handle_error("Invalid credentials", 401)

            elif self.path == "/register":
                required_fields = ["username", "password", "full_name", "currency"]
                if not all(field in data for field in required_fields):
                    return self._handle_error("Missing required fields", 400)
                
                result = register_user(data["username"], data["password"], data["full_name"], data["currency"])
                if "error" in result:
                    self._handle_error(result["error"], 400)
                else:
                    self._send_json(result)

            elif self.path == "/transactions/add":
                if not data:
                    return self._handle_error("Missing transaction data", 400)
                add_transaction(data)
                self._send_json({"success": True})

            else:
                self._handle_error("Invalid endpoint", 404)

        except json.JSONDecodeError:
            self._handle_error("Invalid JSON data", 400)
        except Exception as e:
            self._handle_error(str(e), 500)

    def do_GET(self):
        try:
            if self.path.startswith("/transactions"):
                try:
                    username = self.path.split("?user=")[1]
                    txs = get_user_transactions(username)
                    self._send_json(txs)
                except IndexError:
                    self._handle_error("Missing user parameter", 400)
            else:
                self._handle_error("Invalid endpoint", 404)
        except Exception as e:
            self._handle_error(str(e), 500)

    def do_DELETE(self):
        try:
            if self.path.startswith("/transactions/delete"):
                try:
                    tx_id = parse_qs(self.path.split("?")[1])["id"][0]
                    if delete_transaction(tx_id):
                        self._send_json({"success": True})
                    else:
                        self._handle_error("Transaction not found", 404)
                except (IndexError, KeyError):
                    self._handle_error("Missing transaction ID", 400)
            else:
                self._handle_error("Invalid endpoint", 404)
        except Exception as e:
            self._handle_error(str(e), 500)

def run():
    print(f"Server running on http://{HOST}:{PORT}")
    HTTPServer((HOST, PORT), SimpleAPI).serve_forever()

if __name__ == "__main__":
    run()
