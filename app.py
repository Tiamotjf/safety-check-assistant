"""Standard-library server; listen on loopback only. No outbound requests."""
import argparse
import json
import secrets
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from engine import Engine, Rejected

BASE = Path(__file__).resolve().parent
SESSIONS = {}
LOCK = threading.Lock()

class Handler(BaseHTTPRequestHandler):
    def session(self):
        cookies = dict(x.strip().split("=", 1) for x in self.headers.get("Cookie", "").split(";") if "=" in x)
        sid = cookies.get("safety_session")
        if sid not in SESSIONS:
            sid = secrets.token_hex(24)
            SESSIONS[sid] = Engine()
        return sid, SESSIONS[sid]

    def reply(self, data, status=200, sid=None, content_type="application/json"):
        payload = json.dumps(data).encode() if content_type == "application/json" else data
        self.send_response(status)
        self.send_header("Content-Type", content_type + "; charset=utf-8")
        self.send_header("Content-Length", str(len(payload)))
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("Content-Security-Policy", "default-src 'self'; script-src 'self'; style-src 'self'; connect-src 'self'; frame-ancestors 'none'")
        if sid:
            self.send_header("Set-Cookie", f"safety_session={sid}; HttpOnly; SameSite=Strict; Path=/")
        self.end_headers()
        self.wfile.write(payload)

    def do_GET(self):
        with LOCK:
            if self.path == "/api/state":
                sid, engine = self.session()
                return self.reply(engine.state(), sid=sid)
        paths = {"/": ("index.html", "text/html"), "/app.js": ("app.js", "application/javascript"), "/style.css": ("style.css", "text/css")}
        if self.path in paths:
            filename, mime = paths[self.path]
            return self.reply((BASE / "web" / filename).read_bytes(), content_type=mime)
        return self.reply({"error": "Not found"}, 404)

    def do_POST(self):
        # JS sends JSON plus a non-simple header; do not accept cross-origin requests.
        host = self.headers.get("Host", "")
        if self.headers.get("Origin") not in (None, "http://" + host) or self.headers.get("X-Local-Review") != "1":
            return self.reply({"error": "Local interface requests only."}, 403)
        try:
            size = int(self.headers.get("Content-Length", "0"))
            if not 0 < size <= 10000:
                raise Rejected("Invalid request size.")
            data = json.loads(self.rfile.read(size))
            if not isinstance(data, dict):
                raise Rejected("JSON object required.")
            with LOCK:
                sid, engine = self.session()
                if self.path == "/api/scenario":
                    engine.reset(data.get("scenario"))
                    result = engine.state()
                elif self.path == "/api/prepare":
                    result = engine.prepare()
                elif self.path == "/api/draft":
                    result = engine.edit(data)
                elif self.path == "/api/acknowledge":
                    result = engine.acknowledge(data.get("reason"))
                elif self.path == "/api/review":
                    result = {"token": engine.review(data.get("revision"), data.get("checked"))}
                elif self.path == "/api/send":
                    result = engine.send(data.get("token"))
                elif self.path == "/api/cancel":
                    result = engine.cancel()
                elif self.path == "/api/failure":
                    if engine.stage != "review" or not isinstance(data.get("fail"), bool):
                        raise Rejected("Failure fixture requires an open draft and a Boolean value.")
                    engine.fail_next = data["fail"]
                    engine.event("failure_fixture_set", enabled=engine.fail_next)
                    result = engine.state()
                else:
                    return self.reply({"error": "Not found"}, 404)
                return self.reply(result, sid=sid)
        except (Rejected, ValueError, TypeError) as exc:
            return self.reply({"error": str(exc)}, 400)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", type=int, default=8765)
    args = parser.parse_args()
    server = ThreadingHTTPServer(("127.0.0.1", args.port), Handler)
    print(f"Local prototype: http://127.0.0.1:{args.port} (no real email)", flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        server.server_close()
