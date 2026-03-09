from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
from pathlib import Path
import json

BASE = Path(__file__).resolve().parent.parent
STATIC_DIR = BASE / "dashboard" / "static"
TEMPLATE_DIR = BASE / "dashboard" / "templates"
LEDGER_FILE = BASE / "ledger.json"

def load_ledger():
    if LEDGER_FILE.exists():
        return json.loads(LEDGER_FILE.read_text())
    return []

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed = urlparse(self.path)
        if parsed.path == "/":
            with open(TEMPLATE_DIR / "dashboard.html") as f:
                html = f.read()
            self._respond(200, "text/html", html.encode())
            return
        if parsed.path == "/api/status":
            ledger = load_ledger()
            orgs = {}
            for entry in ledger:
                org = entry.get("org", "unknown")
                orgs.setdefault(org, []).append(entry)
            result = [{"org": o, **entries[-1]} for o, entries in orgs.items()]
            self._respond(200, "application/json", json.dumps(result).encode())
            return
        if parsed.path == "/api/timeline":
            qs = parse_qs(parsed.query)
            org = qs.get("org", [None])[0]
            ledger = load_ledger()
            if org:
                ledger = [e for e in ledger if e.get("org") == org]
            self._respond(200, "application/json", json.dumps(ledger).encode())
            return
        if parsed.path.startswith("/static/"):
            file = STATIC_DIR / parsed.path.split("/static/")[1]
            if file.exists():
                ct = "text/css" if file.suffix == ".css" else "application/javascript"
                self._respond(200, ct, file.read_bytes())
                return
        self._respond(404, "text/plain", b"Not found")

    def _respond(self, code, ct, body):
        self.send_response(code)
        self.send_header("Content-Type", ct)
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, *args):
        pass

if __name__ == "__main__":
    server = HTTPServer(("0.0.0.0", 8080), Handler)
    print("Serving on http://localhost:8080")
    server.serve_forever()
