from aiogram import Bot
from aiogram.types import BotCommand
from aiogram.utils.i18n import gettext as _


async def set_bot_commands(bot: Bot):
    commands = [
        BotCommand(command='/start', description=_('Botni ishga tushirish uchun')),
        BotCommand(command='/register', description=_("Ro'yxatdan o'tish uchun")),
        BotCommand(command='/login', description=_('Akkauntga kirish uchun')),
        BotCommand(command='/delete_account', description=_("Akkauntni o'chirish uchun")),
        BotCommand(command='/logout', description=_("Akkauntdan chiqish")),
        BotCommand(command='/help', description=_("Yordam")),
        BotCommand(command='/change_username', description=_("Usernameni o'zgartirish uchun")),
        BotCommand(command='/change_password', description=_("Parolni o'zgartirish uchun")),
    ]

    await bot.set_my_commands(commands=commands)
