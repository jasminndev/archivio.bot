import asyncio
import sys

from aiogram import Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from bot.commands import set_bot_commands
from bot.handler import *
from bot.handler.add_media.documents import router_document
from bot.handler.add_media.photos import router_photo
from bot.handler.add_media.videos import router_video
from bot.handler.add_media.voices import router_voice
from db.config import conf

# r = Redis()
# redis = Redis


BOT_TOKEN = conf.bot.BOT_TOKEN


async def main() -> None:
    dp.include_router(router_photo)
    dp.include_router(router_video)
    dp.include_router(router_document)
    dp.include_router(router_voice)
    bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await set_bot_commands(bot)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
