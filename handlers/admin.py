import logging
from loader import dp, bot
from aiogram import types, Dispatcher
from aiogram.types import CallbackQuery
from keyboards.default_keyboard import admin_menu
from aiogram.dispatcher import FSMContext, Dispatcher
from aiogram.dispatcher import filters
from aiogram.types import InputFile
from aiogram.dispatcher.filters.state import State, StatesGroup
from database.work_with_db import DataBase
from pathlib import Path


myself = Path(__file__).resolve()
db = DataBase()

logger = logging.getLogger('app.handlers.admin')

class UserBlock(StatesGroup):
	user_id = State()

class ChangeBalance(StatesGroup):
	user_id = State()
	new_balance = State()



async def admin(message : types.Message):
	if await db.check_permission():
		await message.answer(f'Привет, {message.from_user.first_name}!')
		await message.answer('Вы находитесь в режиме администратора', reply_markup = admin_menu)



async def user_block(message : types.Message, state : FSMContext):    	
	if message.text == "⚖️Заблокировать пользователя":
		await UserBlock.user_id.set()
		await bot.send_message(message.from_user.id, 'Введите id пользователя, которого хотите заблокировать: ')

@dp.message_handler(content_types = ['text'], state=UserBlock.user_id)
async def enter_id(message : types.Message, state : FSMContext):
	async with state.proxy() as data:
		data["user_id"] = message.text
	async with state.proxy() as data:
		await db.change_permission(data["user_id"])
		await bot.send_message(message.from_user.id, f'Пользователь {data["user_id"]} заблокирован')
	await state.finish()



async def change_balance(message : types.Message, state : FSMContext):    	
	if message.text == "💳Изменить баланс пользователя":
		await ChangeBalance.user_id.set()
		await bot.send_message(message.from_user.id, 'Введите id пользователя, баланс которого хотите изменить: ')

@dp.message_handler(content_types = ['text'], state=ChangeBalance.user_id)
async def change_balance_set(message : types.Message, state : FSMContext):
	async with state.proxy() as data:
		data["user_id"] = message.text
	await ChangeBalance.next()
	await message.answer("Введите сумму нового баланса: ")

@dp.message_handler(content_types = ['text'], state=ChangeBalance.new_balance)
async def change_balance_user_id(message : types.Message, state : FSMContext):
	async with state.proxy() as data:
		data["new_balance"] = message.text
	async with state.proxy() as data:
		await db.change_balance(data["user_id"], data["new_balance"])
		await bot.send_message(message.from_user.id, f'Баланс успешно изменен, новый баланс id: {data["user_id"]} составляет - {data["new_balance"]}')
	await state.finish()




async def admin_menu_handler(message : types.Message):
	if message.text == "📋Список пользователей":
		user_list = await db.get_user_list()
		for user in user_list:
			await message.answer(f'id: {user[0]} balance: {user[1]}')

	elif message.text == "📤Выгрузка логов":
		try:
			with open('logs/all_info.log', 'rb') as file:
				await bot.send_document(message.from_user.id, ('all_info.log', file))
		except Exception as ex:
			logger.info(ex)
		try:
			with open('logs/only_warnings.log', 'rb') as file:
				await bot.send_document(message.from_user.id, ('all_info.log', file))
		except Exception as ex:
			logger.info(ex)



def register_handlers_admin(dp : Dispatcher):
	dp.register_message_handler(admin, commands = ["admin"])
	dp.register_message_handler(user_block, filters.Text(startswith = '⚖️Заблокировать'))
	dp.register_message_handler(change_balance, filters.Text(startswith = '💳Изменить'))
	dp.register_message_handler(admin_menu_handler)
	