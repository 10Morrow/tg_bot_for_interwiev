from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

top_up_balance = InlineKeyboardMarkup(
	inline_keyboard = [[InlineKeyboardButton(text="Пополнить баланс", callback_data="top_up")]]
	)


def payment_btns(pay_info):
	payment_info = str(pay_info[1])+'::'+str(pay_info[2])
	payment = InlineKeyboardMarkup(
		inline_keyboard = [
		[InlineKeyboardButton(text="Оплатить", url = pay_info[0])],
		[InlineKeyboardButton(text="Проверить оплату", callback_data=payment_info)]
		]
		)
	return payment