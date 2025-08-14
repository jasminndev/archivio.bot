import asyncio
import sys

from aiogram import Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from bot.commands import set_bot_commands
from bot.handler import *
from bot.handler.add_media.photos import router
from db.config import conf

# r = Redis()
# redis = Redis


BOT_TOKEN = conf.bot.BOT_TOKEN


async def main() -> None:
    dp.include_router(router)
    bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await set_bot_commands(bot)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
