"""A tiny web server so anything that can send an HTTP request can use the agent.

  POST /agents            {"request": "...", "callback": "https://..."}  -> launch
  GET  /agents/<id>                                                      -> status
  POST /agents/<id>/reply {"answer": "yes"}                              -> answer a question or approval

Run it:  python lessons/11-trigger-from-anywhere/starter/server.py
"""
import json
import sys
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

import triggers  # noqa: E402

from shared.llm import ask_llm  # noqa: E402

human = triggers.human


def make_server(outbox: list, store: Path = triggers.DEFAULT_STORE, ask=ask_llm, port: int = 8000):
    class Handler(BaseHTTPRequestHandler):
        def _send(self, code: int, body: dict) -> None:
            data = json.dumps(body).encode()
            self.send_response(code)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(data)))
            self.end_headers()
            self.wfile.write(data)

        def _json(self) -> dict:
            length = int(self.headers.get("Content-Length", 0))
            return json.loads(self.rfile.read(length) or b"{}")

        def do_POST(self):
            parts = self.path.strip("/").split("/")
            try:
                if parts == ["agents"]:
                    self._send(200, triggers.from_webhook(self._json(), outbox, store, ask))
                elif len(parts) == 3 and parts[0] == "agents" and parts[2] == "reply":
                    self._send(200, triggers.handle_reply(parts[1], self._json().get("answer", ""), outbox, store, ask))
                else:
                    self._send(404, {"error": "not found"})
            except (ValueError, KeyError, FileNotFoundError) as err:
                self._send(400, {"error": str(err)})

        def do_GET(self):
            parts = self.path.strip("/").split("/")
            try:
                if len(parts) == 2 and parts[0] == "agents":
                    self._send(200, human.get_status(parts[1], store))
                else:
                    self._send(404, {"error": "not found"})
            except FileNotFoundError:
                self._send(404, {"error": "no such agent"})

        def log_message(self, *args):  # keep the console quiet
            pass

    return ThreadingHTTPServer(("127.0.0.1", port), Handler)


if __name__ == "__main__":
    server = make_server(outbox=[])
    print("Listening on http://127.0.0.1:8000 (Ctrl+C to stop)")
    server.serve_forever()
