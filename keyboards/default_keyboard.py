# -*- coding: utf-8 -*-
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

admin_menu = ReplyKeyboardMarkup(
keyboard=[
	[KeyboardButton(text="📋Список пользователей")],
	[KeyboardButton(text="⚖️Заблокировать пользователя")],
	[KeyboardButton(text="📤Выгрузка логов")],
	[KeyboardButton(text="💳Изменить баланс пользователя")]
	]
	,resize_keyboard = True
	)
