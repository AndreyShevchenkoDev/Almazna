import time
import requests
from state import get_status, get_balance, get_report, get_day, get_month, get_info
from phrases import unexpected_error

TELEGRAM_TOKEN = "7058796866:AAFxp1h5uqIqWkn7T-1bLtrWASp3mu8zwpQ"
CHAT_ID = "5749742792"
BASE_URL = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}"

def send_update(message):
    url = f"{BASE_URL}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": message
    }
    try:
        response = requests.post(url, json=payload)
        print(f"✅ Уведомление: {message}")
    except Exception as e:
        print(f"❌ Ошибка Telegram: {e}")

def check_for_commands():
    print("🛰️ Ожидание команд от господина...")
    last_update_id = None

    while True:
        try:
            params = {'timeout': 10}
            if last_update_id:
                params['offset'] = last_update_id + 1

            url = f"{BASE_URL}/getUpdates"
            response = requests.get(url, params=params).json()
            updates = response.get("result", [])

            for update in updates:
                message = update.get("message")
                if not message or "text" not in message:
                    continue  # игнорируем не текстовые

                chat_id = message["chat"]["id"]
                text = message["text"].strip()
                update_id = update["update_id"]

                if chat_id != int(CHAT_ID):
                    print("⚠️ Команда не от владельца. Игнорирую.")
                    continue

                print(f"📩 Команда получена: {text}")
                last_update_id = update_id  # запомнить последнее обработанное

                # Обработка команд:
                if text == "/status":
                    send_update(get_status())
                elif text == "/balance":
                    send_update(get_balance())
                elif text == "/report":
                    send_update(get_report())
                elif text == "/start":
                    send_update("👑 С шахты начинается ваше Величие.\n"
                                "💎 Добро пожаловать, господин Андрей.\n"
                                "🏰 Алмазная Империя готова к приумножению богатств.\n"
                                "📦 Используйте команды: /balance, /status, /report")
                elif text == "/day":
                    send_update(get_day())
                elif text == "/month":
                    send_update(get_month())
                elif text == "/info":
                    send_update(get_info())
                else:
                    print(f"❓ Неизвестная команда: {text} — игнорируется.")

            time.sleep(1)

        except Exception as e:
            print("❗ Ошибка в цикле команд:", e)
            send_update(unexpected_error())
            time.sleep(5)