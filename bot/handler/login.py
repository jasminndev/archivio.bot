from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.utils.i18n import gettext as _

from bot.dispatcher import dp
from bot.states import LoginStates
from db.model import User, get_db


@dp.message(Command("login"))
async def command_login(message: Message, state: FSMContext):
    await message.answer(_("📝 Please, enter your username"))
    await state.set_state(LoginStates.username)


@dp.message(LoginStates.username)
async def process_username(message: Message, state: FSMContext):
    await state.update_data(username=message.text)
    await message.answer(_("🔒 Now, enter your password"))
    await state.set_state(LoginStates.password)


@dp.message(LoginStates.password)
async def process_password(message: Message, state: FSMContext):
    with get_db() as db:
        data = await state.get_data()
        username = data.get('username')

        user = db.query(User).filter(User.username == username).first()

        if not user:
            await message.answer(_("❌ No such user found!"))
            await state.set_state(LoginStates.username)

        elif message.text.strip() != user.password:
            await message.answer(_("❌ Invalid password! Please try again."))
            await state.set_state(LoginStates.password)

        else:
            rkb = ReplyKeyboardBuilder()
            rkb.add(KeyboardButton(text=_("🏠 Main menu")))
            rkb.adjust(1,1)
            rkb = rkb.as_markup(resize_keyboard=True)
            await state.set_state()
            await message.answer(_("✅ You have successfully logged in."), reply_markup=rkb)
            await state.clear()
