import json
import os
import yfinance as yf

# Файл для хранения цен
PRICE_FILE = "prices.json"

# Активы из твоего портфеля
TICKERS = [
    "NVDA", "AMD", "AVGO", "MSFT", "ORCL", "PLTR", "PANW",
    "CRWD", "NFLX", "BRK-B", "MELI", "UBER", "BTC-USD", "ETH-USD"
]

def fetch_prices():
    print("⏳ Загружаю цены с Yahoo Finance...")
    prices = {}
    for ticker in TICKERS:
        try:
            yf_ticker = yf.Ticker(ticker)
            data = yf_ticker.history(period="1d")
            if not data.empty:
                close_price = data['Close'].iloc[-1]
                prices[ticker] = round(close_price, 2)
                print(f"  {ticker}: {close_price}")
            else:
                print(f"⚠️ Нет данных для {ticker}")
        except Exception as e:
            print(f"❌ Ошибка загрузки {ticker}: {e}")

    return prices

def save_prices(prices):
    with open(PRICE_FILE, "w") as f:
        json.dump(prices, f, indent=2)
    print(f"✅ Цены сохранены в {PRICE_FILE}")

def load_prices():
    if not os.path.exists(PRICE_FILE) or os.path.getsize(PRICE_FILE) == 0:
        print(f"⚠️ Файл {PRICE_FILE} отсутствует или пустой")
        return {}
    try:
        with open(PRICE_FILE, "r") as f:
            prices = json.load(f)
            return prices
    except json.JSONDecodeError:
        print(f"❌ Ошибка разбора JSON в {PRICE_FILE}")
        return {}

def update_prices():
    prices = fetch_prices()
    if prices:
        save_prices(prices)
    else:
        print("❌ Не удалось обновить цены — данные отсутствуют")

if __name__ == "__main__":
    update_prices()
