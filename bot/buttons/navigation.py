from aiogram import F
from aiogram.fsm.context import FSMContext
from aiogram.types import KeyboardButton, Message
from aiogram.utils.i18n import gettext as _, lazy_gettext as __
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from bot.dispatcher import dp
from bot.states import SectorStates


def get_add_view_keyboard():
    rkb = ReplyKeyboardBuilder()
    rkb.add(
        KeyboardButton(text=_("⏬ Add")),
        KeyboardButton(text=_("👀 View")),
        KeyboardButton(text=_("⬅️ Back")))
    rkb.adjust(2, 1)
    return rkb.as_markup(resize_keyboard=True)


def navigation_keyboard(include_back=False, include_cancel=False):
    rkb = ReplyKeyboardBuilder()

    rkb.add(KeyboardButton(text=_("🏠 Main menu")))

    if include_back:
        rkb.add(KeyboardButton(text=_("🔙 Back")))

    if include_cancel:
        rkb.add(KeyboardButton(text=_("❌ Cancel")))

    rkb.adjust(2, 1)
    return rkb.as_markup(resize_keyboard=True)


def get_main_menu_keyboard():
    rkb = ReplyKeyboardBuilder()
    rkb.add(
        KeyboardButton(text=_("🖼 Photos")),
        KeyboardButton(text=_("🎥 Videos")),
        KeyboardButton(text=_("📄 Documents")),
        KeyboardButton(text=_("✉️ Letters")),
    )
    rkb.adjust(2, 2)
    return rkb.as_markup(resize_keyboard=True)


def get_back_keyboard():
    rkb = ReplyKeyboardBuilder()
    rkb.add(KeyboardButton(text=_("⬅️ Back")))
    return rkb.as_markup(resize_keyboard=True)


@dp.message(F.text == __("🏠 Main menu"))
async def universal_main_menu_handler(message: Message, state: FSMContext):
    await state.set_state(SectorStates.main_menu)
    await message.answer(_("🏠 Main menu"), reply_markup=get_main_menu_keyboard())
