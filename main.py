import asyncio
import sys
import os
from aiogram import Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from dotenv import load_dotenv

from bot.handler import *
from bot.handler.photo import router_add_photo

load_dotenv()

TOKEN = os.getenv('TOKEN')


async def main() -> None:
    dp.include_router(router_add_photo)
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
