import threading
import time
import os
from http.server import HTTPServer, BaseHTTPRequestHandler
from scheduler import run_scheduler  # твой основной код, который проверяет цены и отправляет уведомления
from telegram_bot import send_update
import phrases

# Получаем порт от Render или ставим дефолт
PORT = int(os.environ.get("PORT", 8000))

# HTTP Handler — Render требует открытый порт
class SimpleHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"✅ Алмазна бот работает. Все под контролем, мой господин!")

# Запускаем HTTP сервер, чтобы Render не закрывал процесс
def run_http_server():
    server = HTTPServer(('', PORT), SimpleHandler)
    print(f"🌐 HTTP сервер запущен на порту {PORT}")
    server.serve_forever()

# Цикл проверок — каждые 30 минут
def periodic_check(interval=1800):  # 30 мин = 1800 сек
    while True:
        print("🔍 Запускаю проверку портфеля...")
        run_scheduler()
        print(f"⏳ Следующая проверка через {interval // 60} минут.")
        time.sleep(interval)

if __name__ == "__main__":
    print("▶️ Алмазна запущена")
    send_update(phrases.greet())  # Первое приветствие

    # Запускаем HTTP сервер в отдельном потоке (чтобы Render видел открытый порт)
    threading.Thread(target=run_http_server, daemon=True).start()

    # Основной цикл проверок
    periodic_check()
