from aiogram import F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.utils.i18n import gettext as _, lazy_gettext as __

from bot.buttons.navigation import get_settings_keyboard
from bot.dispatcher import dp
from bot.states import SectorStates


@dp.message(F.text == __("⚙️ Settings"))
async def settings(message: Message, state: FSMContext):
    await state.set_state(SectorStates.settings)
    await message.answer(_("⚙️ Settings"), reply_markup=get_settings_keyboard())
