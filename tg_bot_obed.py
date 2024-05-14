#!/usr/bin/python
# This is an example file to create quiz polls
import telebot
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
import pytz

API_TOKEN = "6286082728:AAFQxrXyE4F74QOCJQ-QMofEPKi3q9hcIto"
bot = telebot.TeleBot(API_TOKEN)

# @bot.message_handler(commands=["poll"])
# def create_poll(message):
#     answer_options = ["Еду", "Не"]
#     bot.send_poll(
#         chat_id=message.chat.id,
#         question="Кушать едем?",
#         options=answer_options,
#         type="regular",
#         is_anonymous=False,
#     )

def send_daily_poll():
    chat_id = "532929414"  # Замените на ваш chat_id
    question = "Ваш вопрос"
    options = ["Вариант 1", "Вариант 2"]
    bot.send_poll(chat_id=chat_id, question=question, options=options, type="regular")

# Создаем экземпляр планировщика
scheduler = BackgroundScheduler()
# Настраиваем часовой пояс
timezone = pytz.timezone("Europe/Moscow")
# Добавляем задачу в планировщик.
# trigger='cron' используется для задания периодических задач
scheduler.add_job(send_daily_poll, trigger='cron', day_of_week='mon-fri', hour=20, minute=47, timezone=timezone)

# Запускаем планировщик
scheduler.start()

# ... (остальная часть вашего кода)
# @bot.poll_answer_handler()
# def handle_poll(poll):
    # This handler can be used to log User answers and to send next poll
    # pass

# bot.infinity_polling()

# Не забудьте вызвать scheduler.shutdown() когда планировщик больше не будет нужен