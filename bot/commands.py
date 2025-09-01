from aiogram import Bot
from aiogram.types import BotCommand


async def set_bot_commands(bot: Bot):
    commands = [
        BotCommand(command='/start', description='Botni ishga tushirish uchun'),
        BotCommand(command='/register', description="Ro'yxatdan o'tish uchun"),
        BotCommand(command='/login', description='Akkauntga kirish uchun'),
        BotCommand(command='/help', description="Yordam"),
    ]
    await bot.set_my_commands(commands=commands)
