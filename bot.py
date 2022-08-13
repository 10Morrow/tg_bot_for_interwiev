# -*- coding: utf-8 -*-
import logging
from loader import bot , dp, admin_id
from aiogram.utils import executor

logger = logging.getLogger('app.bot')

async def on_startup(dp):
	logger.info('the bot started working')
	await bot.send_message(admin_id, "the bot started working")

async def on_shutdown(dp):
	logger.info('bot close')
	await bot.close()


from handlers import client, admin
client.register_handlers_clients(dp)
admin.register_handlers_admin(dp)


if __name__ == "__main__":
	executor.start_polling(dp, skip_updates=True, on_startup = on_startup, on_shutdown = on_shutdown)