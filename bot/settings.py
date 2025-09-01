from aiogram import F
from aiogram.types import Message
from aiogram.utils.i18n import gettext as __

from bot.dispatcher import dp


@dp.message(F.text == __("⚙️ Settings"))
async def settings(message: Message):
    pass