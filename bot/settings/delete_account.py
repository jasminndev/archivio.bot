from aiogram import F
from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from aiogram.types import Message
from aiogram.utils.i18n import gettext as _, lazy_gettext as __

from bot.buttons.navigation import delete_account_markup, get_settings_keyboard
from bot.states import SectorStates
from db.models import User

delete_account_router = Router()


@delete_account_router.message(SectorStates.settings, F.text == __("🏌🏻‍♀️ Delete account"))
async def delete_account_button(message: Message, state: FSMContext):
    await state.set_state(SectorStates.delete_user)
    await message.answer(
        _("Do you really want to delete your account?\nAfter deleting, you won’t be able to restore it!"),
        reply_markup=delete_account_markup()
    )


@delete_account_router.callback_query(SectorStates.delete_user, F.data == "delete_yes")
async def confirm_delete(callback: CallbackQuery, state: FSMContext):
    tg_id = str(callback.from_user.id)
    user = await User.filter_one(tg_id=tg_id)
    if user:
        await User.delete(_id=user.id)

    await state.clear()
    await callback.message.edit_text(
        _("🗑 Your account has been deleted successfully.")
    )


@delete_account_router.callback_query(SectorStates.delete_user, F.data == "delete_cancel")
async def cancel_delete(callback: CallbackQuery, state: FSMContext):
    await state.set_state(SectorStates.settings)
    await callback.message.edit_text(
        _("❌ Account deletion cancelled.")
    )
    await callback.message.answer(_("⚙️ Settings"), reply_markup=get_settings_keyboard())
