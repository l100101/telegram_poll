import asyncio
import logging
from aiogram import Bot
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import pytz
from datetime import datetime

# Конфигурация
BOT_TOKEN = "token"  # Токен бота
CHAT_ID = -1234567890  # ID чата
PUBLISH_TIME = "11:11"  # Время публикации опроса
PUBLISH_TIMEZONE = "Europe/Samara"  # Часовой пояс

#POLL_TEXT = "Едем в столовку?"  # Текст опроса
#POLL_OPTIONS = ["Плов 11:30", "Воткинск 12:00", "NaN"]  # Варианты ответов
POLL_TEXT = "Едем в столовку?"  # Текст опроса
POLL_OPTIONS = ["Плов 11:30", "Воткинск 12:00", "NaN"]  # Варианты ответов

POLL_PUBLIC = True  # True, если опрос публичный, False, если нет. В каналах опросы всегда анонимные

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

bot = Bot(token=BOT_TOKEN)
scheduler = AsyncIOScheduler()

job_defaults = {
    'misfire_grace_time': 300  # Максимальная допустимая задержка в секундах
}

async def publish_poll():
    try:
        logger.info("Публикация опроса началась")
        poll = await bot.send_poll(
            chat_id=CHAT_ID, question=POLL_TEXT, options=POLL_OPTIONS, is_anonymous=not POLL_PUBLIC,
        )
        logger.info("Опрос опубликован: %s", poll.get_url())
    except Exception as e:
        logger.error("Ошибка при публикации опроса: %s", e)

if __name__ == "__main__":
    try:
        # Лог текущего времени сервера и запланированного времени
        current_time = datetime.now(pytz.timezone(PUBLISH_TIMEZONE)).strftime('%Y-%m-%d %H:%M:%S')
        logger.info("Текущее время сервера: %s", current_time)

        hour, minute = PUBLISH_TIME.split(":")
        scheduler.add_job(
            publish_poll,
            "cron",
            hour=int(hour),
            minute=int(minute),
            timezone=pytz.timezone(PUBLISH_TIMEZONE),
        )
        logger.info("Задача запланирована на %s:%s", hour, minute)
        scheduler.start()
        logger.info("Запланированная задача успешно запущена")
        
        # Проверка запланированных задач
        for job in scheduler.get_jobs():
            logger.info("Запланированная задача: %s", job)
        
        asyncio.get_event_loop().run_forever()
    except Exception as e:
        logger.error("Ошибка при запуске планировщика: %s", e)
