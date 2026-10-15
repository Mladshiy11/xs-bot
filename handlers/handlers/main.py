# main.py
# XS Mobile Numbers Bot — asosiy fayl

import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from config import BOT_TOKEN
import database as db

from handlers import start, menu, companies, search, admin

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(name)


async def main():
    # Bazani ishga tushirish
    await db.init_db()
    logger.info("Ma'lumotlar bazasi tayyor")

    # Botni yaratish
    bot = Bot(
        token=BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )

    # Dispatcher
    dp = Dispatcher()

    # Handlerlarni ulash (tartib muhim!)
    dp.include_router(admin.router)      # admin birinchi
    dp.include_router(start.router)      # start
    dp.include_router(menu.router)       # menu
    dp.include_router(companies.router)  # kompaniyalar
    dp.include_router(search.router)     # qidiruv

    logger.info("Bot ishga tushdi...")

    # Pollingni boshlash
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if name == "main":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info("Bot to'xtatildi")
