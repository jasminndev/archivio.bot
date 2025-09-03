import asyncio
import sys

from aiogram import Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from bot.commands import set_bot_commands
from bot.handler import *
from bot.handler.add_media.audios import router_audio
from bot.handler.add_media.contacts import router_contact
from bot.handler.add_media.documents import router_document
from bot.handler.add_media.photos import router_photo
from bot.handler.add_media.texts import router_text_message
from bot.handler.add_media.videos import router_video
from bot.handler.add_media.voices import router_voice
from bot.handler.settings import router_username
from bot.handler.view_media.audios import router_view_audio
from bot.handler.view_media.contacts import router_view_contact
from bot.handler.view_media.documents import router_view_document
from bot.handler.view_media.photos import router_view_photo
from bot.handler.view_media.texts import router_view_text_message
from bot.handler.view_media.videos import router_view_video
from bot.handler.view_media.voices import router_view_voice
from db.config import conf

# r = Redis()
# redis = Redis


BOT_TOKEN = conf.bot.BOT_TOKEN


async def main() -> None:
    dp.include_router(router_photo)
    dp.include_router(router_video)
    dp.include_router(router_document)
    dp.include_router(router_voice)
    dp.include_router(router_audio)
    dp.include_router(router_contact)
    dp.include_router(router_text_message)
    dp.include_router(router_view_photo)
    dp.include_router(router_view_video)
    dp.include_router(router_view_document)
    dp.include_router(router_view_text_message)
    dp.include_router(router_view_voice)
    dp.include_router(router_view_audio)
    dp.include_router(router_view_contact)
    dp.include_router(router_username)
    bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await set_bot_commands(bot)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
