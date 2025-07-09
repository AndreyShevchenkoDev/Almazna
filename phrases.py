from datetime import datetime
import random

def greet():
    greetings = [
        "💎 Алмазна к вашим услугам, мой господин.",
    ]
    return random.choice(greetings)

def crypto_day():
    return "💰 Сегодня день криптоинвестиций. Приступаю к закупке в ваших интересах."

def stocks_day():
    return "💼 В этот день мы укрепляем позиции в акциях. С вашего позволения, я начну покупку."

def not_today():
    today = datetime.now().strftime("%d.%m.%Y")
    return f"📆 Сегодня {today}. Закупка не запланирована. Алмазна ожидает приказа."

def report_profit(pct, euro):
    return f"📈 Прибыль за сегодня составила {euro:.2f}€ ({pct:.2f}%). Позвольте поздравить."

def report_loss(pct, euro):
    return f"📉 Убыток за сегодня: {euro:.2f}€ ({pct:.2f}%). Алмазна подготовит корректировку."

def rebalance_notice():
    return "⚖️ Провожу балансировку портфеля согласно заданным пропорциям."

def shutdown():
    return "🔒 Алмазна завершила работу. Активы под защитой, как всегда."

def unexpected_error():
    return "❗ Возникла непредвиденная ошибка. Алмазна сообщает об этом незамедлительно."
