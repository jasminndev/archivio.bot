from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery
from aiogram.utils.i18n import gettext as _

from db.models import User


class AuthMiddleware(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[Any, Dict[str, Any]], Awaitable[Any]],
            event: Any,
            data: Dict[str, Any],
    ) -> Any:
        tg_id = None

        if isinstance(event, Message):
            tg_id = str(event.from_user.id)
        elif isinstance(event, CallbackQuery):
            tg_id = str(event.from_user.id)

        if not tg_id:
            return await handler(event, data)

        user = await User.filter(tg_id=tg_id).first()
        if not user:
            if isinstance(event, Message):
                await event.answer(_("⚠️ You are not logged in. Please /start to register."))
            elif isinstance(event, CallbackQuery):
                await event.message.answer(_("⚠️ You are not logged in. Please /start to register."))
            return

        data["user"] = user
        return await handler(event, data)
