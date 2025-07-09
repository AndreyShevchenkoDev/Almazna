from scheduler import run_scheduler
from telegram_bot import send_update, check_for_commands
import phrases
import threading

print("▶️ Алмазна запущена")
send_update(phrases.greet())

threading.Thread(target=check_for_commands, daemon=True).start()
run_scheduler()

while True:
    pass
