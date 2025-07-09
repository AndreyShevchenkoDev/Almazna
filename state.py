import json
import os
from datetime import datetime
from portfolio import TARGET_WEIGHTS

LAST_PURCHASE = {t: None for t in TARGET_WEIGHTS.keys()}

def load_current_values():
    if not os.path.exists("prices.json") or os.path.getsize("prices.json") == 0:
        print("❌ prices.json не найден или пуст. Вернём нули.")
        return {t: 0 for t in TARGET_WEIGHTS.keys()}
    try:
        with open("prices.json", "r") as f:
            prices = json.load(f)
        normalized = {
            "BRK.B": prices.get("BRK-B", 0),
            "BTC": prices.get("BTC-USD", 0),
            "ETH": prices.get("ETH-USD", 0)
        }
        current_values = {
            "NVDA": prices.get("NVDA", 0),
            "AMD": prices.get("AMD", 0),
            "AVGO": prices.get("AVGO", 0),
            "MSFT": prices.get("MSFT", 0),
            "ORCL": prices.get("ORCL", 0),
            "PLTR": prices.get("PLTR", 0),
            "PANW": prices.get("PANW", 0),
            "CRWD": prices.get("CRWD", 0),
            "NFLX": prices.get("NFLX", 0),
            "BRK.B": normalized["BRK.B"],
            "MELI": prices.get("MELI", 0),
            "UBER": prices.get("UBER", 0),
            "BTC": normalized["BTC"],
            "ETH": normalized["ETH"],
        }
        return current_values
    except Exception as e:
        print(f"❌ Ошибка загрузки current_values: {e}")
        return {t: 0 for t in TARGET_WEIGHTS.keys()}

CURRENT_VALUES = load_current_values()

def get_balance():
    return (
        "💼 Баланс портфеля:\n"
        "- Акции: 1 800€\n"
        "- Криптовалюты: 200€\n"
        "- Всего: 2 000€"
    )

def get_info():
    return "ℹ️ Алмазна готова к действиям. Бот активен и ждёт команд."

def get_day():
    return "📈 За сегодня +0.0% (пример)."

def get_month():
    return "📅 Отчёт за месяц: +0.0% (пример)"

def get_report():
    return (
        "📊 Отчёт по портфелю:\n"
        "💰 Всего внесено: 2000€\n"
        "📈 Текущая стоимость: 2200€\n"
        "🎉 Чистая прибыль: +200€ (+10.00%)"
    )

def get_status():
    now = datetime.now().strftime("%d.%m.%Y %H:%M")
    return f"🟢 Алмазна активна.\n⏰ Последнее обращение: {now}"

def get_history(ticker):
    try:
        with open("prices.json", "r") as f:
            prices = json.load(f)
        history = prices.get(ticker, [])
        # Если формат в prices.json — список цен за дни, иначе пустой список
        # Здесь предполагается, что для каждого тикера лежит список с dict { "date":..., "price":... }
        # Если у тебя просто цены, то можно подстроить
        if isinstance(history, list) and history and isinstance(history[0], dict):
            return [p["price"] for p in history][-30:]
        elif isinstance(history, list) and all(isinstance(x, (int, float)) for x in history):
            return history[-30:]
        else:
            return []
    except Exception:
        return []

def check_trailing_stop(ticker, trailing_pct=0.01):
    prices = get_history(ticker)
    if len(prices) < 5:
        return False

    local_max = max(prices)
    current_price = prices[-1]

    drop = (local_max - current_price) / local_max
    return drop >= trailing_pct

def trailing_buy(category, capital):
    if category == "crypto":
        tickers = ["BTC", "ETH"]
    else:
        tickers = [t for t in TARGET_WEIGHTS if t not in ["BTC", "ETH"]]

    bought = []
    for ticker in tickers:
        last = LAST_PURCHASE.get(ticker)
        if last and last.month == datetime.now().month:
            continue

        if check_trailing_stop(ticker):
            amt = round(capital * TARGET_WEIGHTS[ticker], 2)
            LAST_PURCHASE[ticker] = datetime.now()
            bought.append(f"✅ Куплен {ticker} на {amt}€ (скидка 1% от max)")

    if not bought:
        return "⏳ Сигнала нет. Алмазна ждёт откат."
    return "\n".join(bought)
