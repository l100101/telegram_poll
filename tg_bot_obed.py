#!/usr/bin/python
# This is an example file to create quiz polls
import telebot

API_TOKEN = "6286082728:AAFQxrXyE4F74QOCJQ-QMofEPKi3q9hcIto"

bot = telebot.TeleBot(API_TOKEN)

@bot.message_handler(commands=["poll"])
def create_poll(message):
    answer_options = ["Еду", "Не"]
    bot.send_poll(
        chat_id=message.chat.id,
        question="Кушать едем?",
        options=answer_options,
        type="regular",
        is_anonymous=False,
    )

@bot.poll_answer_handler()
def handle_poll(poll):
    # This handler can be used to log User answers and to send next poll
    pass

bot.infinity_polling()