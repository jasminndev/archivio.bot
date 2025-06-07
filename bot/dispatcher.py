from aiogram import Dispatcher
from aiogram.utils.i18n import I18n, FSMI18nMiddleware

dp = Dispatcher()


i18n = I18n(path="locales", default_locale="en", domain="messages")

dp.update.middleware(FSMI18nMiddleware(i18n))
