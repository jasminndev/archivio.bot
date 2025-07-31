from aiogram import Bot
from aiogram.types import BotCommand


async def set_bot_commands(bot: Bot):
    commands = [
        BotCommand(command='/start', description='Botni ishga tushirish uchun'),
        BotCommand(command='/register', description="Ro'yxatdan o'tish uchun"),
        BotCommand(command='/login', description='Akkauntga kirish uchun'),
        BotCommand(command='/delete_account', description="Akkauntni o'chirish uchun"),
        BotCommand(command='/help', description="Yordam"),
        BotCommand(command='/change_username', description="Usernameni o'zgartirish uchun"),
        BotCommand(command='/change_password', description="Parolni o'zgartirish uchun"),
    ]

    await bot.set_my_commands(commands=commands)
