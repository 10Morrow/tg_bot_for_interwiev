import logging
from loader import dp, bot
from aiogram import types, Dispatcher
from loader import pay_token
from aiogram.types import CallbackQuery
from keyboards.inline import top_up_balance, payment_btns
from aiogram.dispatcher import FSMContext, Dispatcher
from aiogram.dispatcher.filters.state import State, StatesGroup
from payment.qiwi import QIWI
from database.work_with_db import DataBase

db = DataBase()

qiwi_pay = QIWI(pay_token)

logger = logging.getLogger('app.handlers.client')

class ClientFSM(StatesGroup):
	deposit_amount = State()


async def callback(callback_query: types.CallbackQuery, state : FSMContext):
    await bot.answer_callback_query(callback_query.id)
    await ClientFSM.deposit_amount.set()
    await bot.send_message(callback_query.from_user.id, 'Введите сумму:')

async def check_payment_status(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    result = callback_query.data.split('::')
    status = await qiwi_pay.check_status(result[0])
    logger.info(result)
    if status == 'PAID':
    	await bot.send_message(callback_query.from_user.id, 'Поздравляем, оплата прошла успешно!')
    	await db.change_balance(callback_query.from_user.id, float(result[1]))
    else:
    	await bot.send_message(callback_query.from_user.id, 'Ожидаем оплату.')





async def set_deposit_amount(message : types.Message, state : FSMContext):
	async with state.proxy() as data:
		data["deposit_amount"] = message.text
	async with state.proxy() as data:
		pay_info = await qiwi_pay.main(data["deposit_amount"])
		pay_info.append(data["deposit_amount"])
	await message.answer('После оплаты нажмите на кнопку\nПроверить платеж', reply_markup = payment_btns(pay_info))
	await state.finish()


async def start(message : types.Message):
	if not await db.user_exist():
		await db.add_new_user()
	if await db.check_permission():
		await message.answer(f'Привет, {message.from_user.first_name}!',reply_markup=types.ReplyKeyboardRemove())
		await message.answer('Я бот для пополнения баланса.\nНажмите на кнопку чтобы пополнить баланс', reply_markup = top_up_balance)





def register_handlers_clients(dp : Dispatcher):
	dp.register_message_handler(start, commands = ["start"])
	dp.register_callback_query_handler(callback, text = "top_up")
	dp.register_callback_query_handler(check_payment_status)
	dp.register_message_handler(set_deposit_amount,content_types = ['text'], state=ClientFSM.deposit_amount)