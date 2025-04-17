from aiogram import F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.utils.i18n import gettext as _, lazy_gettext as __

from bot.dispatcher import dp
from bot.states import SectorStates


@dp.message(SectorStates.password, F.text == __("🏠 Main menu"))
async def main_menu_handler(message: Message, state: FSMContext):
    rkb = ReplyKeyboardBuilder()
    rkb.add(
        KeyboardButton(text=_("🖼 Photos")),
        KeyboardButton(text=_("🎥 Videos")),
        KeyboardButton(text=_("📄 Documents")),
        KeyboardButton(text=_("✉️ Letters")))
    rkb.adjust(2,2)
    rkb = rkb.as_markup(resize_keyboard=True)
    await state.set_state(SectorStates.main_menu)
    await message.answer(_("🏠 Main menu"), reply_markup=rkb)


@dp.message(SectorStates.main_menu, F.text == __("🖼 Photos"))
async def photos_handler(message: Message, state: FSMContext):
    rkb = ReplyKeyboardBuilder()
    rkb.add(
        KeyboardButton(text=_("⏬ Add")),
        KeyboardButton(text=_("👀 View")))
    rkb.adjust(2)
    rkb = rkb.as_markup(resize_keyboard=True)
    await state.set_state(SectorStates.main_menu)
    await message.answer(_("🖼 Photos"), reply_markup=rkb)


@dp.message(SectorStates.main_menu, F.text == __("🎥 Videos"))
async def photos_handler(message: Message, state: FSMContext):
    rkb = ReplyKeyboardBuilder()
    rkb.add(
        KeyboardButton(text=_("⏬ Add")),
        KeyboardButton(text=_("👀 View")))
    rkb.adjust(2)
    rkb = rkb.as_markup(resize_keyboard=True)
    await state.set_state(SectorStates.main_menu)
    await message.answer(_("🎥 Videos"), reply_markup=rkb)


@dp.message(SectorStates.main_menu, F.text == __("📄 Documents"))
async def photos_handler(message: Message, state: FSMContext):
    rkb = ReplyKeyboardBuilder()
    rkb.add(
        KeyboardButton(text=_("⏬ Add")),
        KeyboardButton(text=_("👀 View")))
    rkb.adjust(2)
    rkb = rkb.as_markup(resize_keyboard=True)
    await state.set_state(SectorStates.main_menu)
    await message.answer(_("📄 Documents"), reply_markup=rkb)


@dp.message(SectorStates.main_menu, F.text == __("✉️ Letters"))
async def photos_handler(message: Message, state: FSMContext):
    rkb = ReplyKeyboardBuilder()
    rkb.add(
        KeyboardButton(text=_("⏬ Add")),
        KeyboardButton(text=_("👀 View")))
    rkb.adjust(2)
    rkb = rkb.as_markup(resize_keyboard=True)
    await state.set_state(SectorStates.main_menu)
    await message.answer(_("✉️ Letters"), reply_markup=rkb)


