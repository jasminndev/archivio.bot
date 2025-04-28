from aiogram.utils.i18n import gettext as _, lazy_gettext as __
from bot.buttons.navigation import get_add_view_keyboard, get_main_menu_keyboard
from bot.states import SectorStates, MainMenu
from bot.handler.lang import *


@dp.message((F.state.in_([MainMenu.photo, MainMenu.video, MainMenu.document, MainMenu.letter, MainMenu.main])),
            F.text.in_([__("⬅️ Back"), __("🏠 Main menu")]))
async def main_menu_handler(message: Message, state: FSMContext):
    await state.set_state(SectorStates.main_menu)
    await message.answer(_("🏠 Main menu"), reply_markup=get_main_menu_keyboard())


@dp.message(SectorStates.main_menu, F.text == __("🖼 Photos"))
async def photos_handler(message: Message, state: FSMContext):
    await state.set_state(MainMenu.photo)
    await message.answer(_("🖼 Photos"), reply_markup=get_add_view_keyboard())


@dp.message(SectorStates.main_menu, F.text == __("🎥 Videos"))
async def videos_handler(message: Message, state: FSMContext):
    await state.set_state(MainMenu.video)
    await message.answer(_("🎥 Videos"), reply_markup=get_add_view_keyboard())


@dp.message(SectorStates.main_menu, F.text == __("📄 Documents"))
async def documents_handler(message: Message, state: FSMContext):
    await state.set_state(MainMenu.document)
    await message.answer(_("📄 Documents"), reply_markup=get_add_view_keyboard())


@dp.message(SectorStates.main_menu, F.text == __("✉️ Letters"))
async def letters_handler(message: Message, state: FSMContext):
    await state.set_state(MainMenu.letter)
    await message.answer(_("✉️ Letters"), reply_markup=get_add_view_keyboard())


