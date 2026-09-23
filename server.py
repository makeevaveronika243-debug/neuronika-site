#!/usr/bin/env python3
"""
Статика сайта + POST /api/lead — отправка заявки в Telegram.
Секреты: файл .env (см. .env.example). Не коммитить .env.
"""
from __future__ import annotations

import json
import os
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from http import HTTPStatus
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from pathlib import Path

ROOT = Path(__file__).resolve().parent
MAX_BODY = 8_192
PHONE_DIGITS_RE = re.compile(r"\D")


def load_dotenv(path: Path) -> None:
    if not path.is_file():
        return
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        if key and key not in os.environ:
            os.environ[key] = value


def phone_digit_count(phone: str) -> int:
    return len(PHONE_DIGITS_RE.sub("", phone))


def escape_telegram(text: str) -> str:
    return (
        text.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
    )


def send_telegram_message(text: str) -> None:
    token = os.environ.get("TELEGRAM_BOT_TOKEN", "").strip()
    chat_id = os.environ.get("TELEGRAM_CHAT_ID", "").strip()
    if not token or not chat_id:
        raise RuntimeError("telegram_not_configured")

    payload = urllib.parse.urlencode(
        {
            "chat_id": chat_id,
            "text": text,
            "parse_mode": "HTML",
            "disable_web_page_preview": "true",
        }
    ).encode("utf-8")
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    req = urllib.request.Request(url, data=payload, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            body = json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")[:200]
        raise RuntimeError(f"telegram_http_{exc.code}: {detail}") from exc

    if not body.get("ok"):
        desc = str(body.get("description", ""))
        raise RuntimeError(f"telegram_api_error: {desc}")


def telegram_client_error(exc: RuntimeError) -> str:
    msg = str(exc).lower()
    if str(exc) == "telegram_not_configured":
        return "not_configured"
    if "401" in msg or "unauthorized" in msg:
        return "invalid_token"
    if "chat not found" in msg:
        return "invalid_chat"
    if "bot was blocked" in msg or "blocked by the user" in msg:
        return "bot_blocked"
    if "group chat was upgraded" in msg:
        return "invalid_chat"
    return "delivery_failed"


class SiteHandler(SimpleHTTPRequestHandler):
    server_version = "NeuroNikaSite/1.0"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(ROOT), **kwargs)

    def log_message(self, format: str, *args) -> None:
        if self.path.startswith("/api/"):
            sys.stderr.write("%s - %s\n" % (self.address_string(), format % args))

    def end_headers(self) -> None:
        self.send_header("X-Content-Type-Options", "nosniff")
        super().end_headers()

    def do_GET(self) -> None:
        # Канонический адрес главной — /, не /index.html
        path = urllib.parse.unquote(self.path.split("?", 1)[0].rstrip("/") or "/")
        if path == "/index.html":
            self.send_response(HTTPStatus.MOVED_PERMANENTLY)
            self.send_header("Location", "/")
            self.end_headers()
            return
        super().do_GET()

    def do_OPTIONS(self) -> None:
        if self.path == "/api/lead":
            self.send_response(HTTPStatus.NO_CONTENT)
            self._cors_headers()
            self.end_headers()
            return
        self.send_error(HTTPStatus.NOT_FOUND)

    def do_POST(self) -> None:
        if self.path != "/api/lead":
            self.send_error(HTTPStatus.NOT_FOUND)
            return

        length = int(self.headers.get("Content-Length", 0))
        if length <= 0 or length > MAX_BODY:
            self._json_response(HTTPStatus.BAD_REQUEST, {"ok": False, "error": "invalid_body"})
            return

        try:
            data = json.loads(self.rfile.read(length).decode("utf-8"))
        except (json.JSONDecodeError, UnicodeDecodeError):
            self._json_response(HTTPStatus.BAD_REQUEST, {"ok": False, "error": "invalid_json"})
            return

        # Honeypot — боты часто заполняют скрытое поле
        if data.get("company"):
            self._json_response(HTTPStatus.OK, {"ok": True})
            return

        name = (data.get("name") or "").strip()
        phone = (data.get("phone") or "").strip()
        contact_method = (data.get("contact_method") or "").strip()

        allowed_methods = {"Telegram", "Телефон", "WhatsApp", "Email"}
        errors: list[str] = []
        if not name or len(name) > 120:
            errors.append("name")
        if not phone or len(phone) > 40 or phone_digit_count(phone) < 10:
            errors.append("phone")
        if contact_method not in allowed_methods:
            errors.append("contact_method")

        if errors:
            self._json_response(
                HTTPStatus.BAD_REQUEST,
                {"ok": False, "error": "validation", "fields": errors},
            )
            return

        page = (data.get("page") or "").strip()[:200]
        text = (
            "<b>Новая заявка с сайта</b>\n"
            f"Имя: {escape_telegram(name)}\n"
            f"Телефон: {escape_telegram(phone)}\n"
            f"Связь: {escape_telegram(contact_method)}"
        )
        if page:
            text += f"\nСтраница: {escape_telegram(page)}"

        try:
            send_telegram_message(text)
        except RuntimeError as exc:
            code = telegram_client_error(exc)
            sys.stderr.write(f"telegram lead error: {code} — {exc}\n")
            if code == "not_configured":
                self._json_response(
                    HTTPStatus.SERVICE_UNAVAILABLE,
                    {"ok": False, "error": code},
                )
                return
            self._json_response(
                HTTPStatus.BAD_GATEWAY,
                {"ok": False, "error": code},
            )
            return

        self._json_response(HTTPStatus.OK, {"ok": True})

    def _cors_headers(self) -> None:
        origin = self.headers.get("Origin")
        host = self.headers.get("Host")
        if origin and host:
            # Только тот же хост (локально и на домене)
            if host in origin:
                self.send_header("Access-Control-Allow-Origin", origin)
                self.send_header("Access-Control-Allow-Methods", "POST, OPTIONS")
                self.send_header("Access-Control-Allow-Headers", "Content-Type")

    def _json_response(self, status: int, payload: dict) -> None:
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self._cors_headers()
        self.end_headers()
        self.wfile.write(body)


def main() -> None:
    load_dotenv(ROOT / ".env")
    port = int(os.environ.get("PORT", "8080"))
    # Слушаем все интерфейсы — иначе localhost (IPv6) может попасть на старый http.server
    server = ThreadingHTTPServer(("", port), SiteHandler)
    print(f"Сервер: http://localhost:{port}/ (статика + POST /api/lead)", flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nОстановка.", flush=True)
        server.server_close()


if __name__ == "__main__":
    main()
