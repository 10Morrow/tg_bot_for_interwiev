# -*- coding: utf-8 -*-
from aiogram import types
from asyncpg import Connection, Record
from asyncpg.exceptions import UniqueViolationError

from loader import bot, dp, db

class DataBase:
	pool: Connection = db

	USER_EXIST = "SELECT * FROM userlist WHERE id = $1"

	ADD_NEW_USER = "INSERT INTO userlist(id, balance, permission) VALUES ($1, 0, true)"

	USER_LIST = "SELECT (id, balance) FROM userlist"

	CHANGE_BALANCE = "UPDATE userlist SET balance = $1 WHERE id = $2"

	BALANCE = "SELECT balance FROM userlist WHERE id = $1"

	INCREASE_BALANCE = "UPDATE userlist SET balance = $1 WHERE id = $2"
	
	CHANGE_PERMISSION = "UPDATE userlist SET permission = $1 WHERE id = $2"

	CHECK_PERMISSION = "SELECT permission FROM userlist WHERE id = $1"


	async def balance(self, user_id):
		user_id = int(user_id)
		user_balance = await self.pool.fetchval(self.BALANCE, user_id)
		return user_balance

	async def increase_balance(self,user_id, new_balance):
		user_id = int(user_id)
		new_balance = self.balance(user_id) + float(new_balance)
		args = new_balance, user_id
		status = await self.pool.fetch(self.CHANGE_BALANCE, *args)


	async def user_exist(self):
		user = types.User.get_current()
		user_id = user.id
		result = await self.pool.fetchval(self.USER_EXIST, user_id)
		return bool(result)

	async def check_permission(self):
		user = types.User.get_current()
		user_id = user.id
		result = await self.pool.fetchval(self.CHECK_PERMISSION, user_id)
		return result

	async def get_user_list(self):
		result = await self.pool.fetch(self.USER_LIST)
		result = [i['row'] for i in result]
		if type(result) != list:
			result = [result]
		id_amount_list = [(person[0],person[1]) for person in result]
		return id_amount_list

	async def add_new_user(self):
		user = types.User.get_current()
		user_id = user.id
		try:
			await self.pool.fetchval(self.ADD_NEW_USER, user_id)
		except UniqueViolationError:
			pass

	async def change_balance(self,user_id, new_balance):
		user_id = int(user_id)
		new_balance = float(new_balance)
		args = new_balance, user_id
		status = await self.pool.fetch(self.CHANGE_BALANCE, *args)

	async def change_permission(self, user_id, status = False):
		user_id = int(user_id)
		args = status, user_id
		await self.pool.fetchval(self.CHANGE_PERMISSION, *args)

