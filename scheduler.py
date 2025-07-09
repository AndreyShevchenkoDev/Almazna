from datetime import datetime
from telegram_bot import send_update
from price_updater import update_prices
from state import trailing_buy
import phrases

def run_scheduler():
    today = datetime.now().day

    # Сначала обновим цены
    update_prices()

    if today >= 3:
        send_update("🔍 Алмазна проверяет крипту...")
        result_crypto = trailing_buy("crypto", 1500 * 0.10)
        send_update(result_crypto)

        send_update("🔍 Алмазна проверяет акции...")
        result_stocks = trailing_buy("stocks", 1500 * 0.90)
        send_update(result_stocks)
    else:
        send_update(phrases.not_today())
