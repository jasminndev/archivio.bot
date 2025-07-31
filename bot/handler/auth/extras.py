from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.utils.i18n import gettext as _

from bot.dispatcher import dp
from db.models import User


@dp.message(Command("delete_account"))
async def command_delete_account(message: Message, state: FSMContext):
    user_id = message.chat.id
    user = await User.filter_one(user_id=user_id)
    if not user:
        await message.answer(_("❌ You are not registered!"))
        return
    await User.delete(_id=user.id)
    await message.answer(_("🗑️ Your account has been deleted."))
