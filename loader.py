# -*- coding: utf-8 -*-
import asyncio
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from asyncio import set_event_loop, new_event_loop
from sql import create_pool
from logs import app_logger
from data import config
# from sql import create_pool


admin_id = config.ADMIN_ID
pay_token = config.PAYMENT_TOKEN

logger = app_logger.get_logger('app')


bot = Bot(token=config.BOT_TOKEN)
dp = Dispatcher(bot, storage = MemoryStorage())


loop = asyncio.get_event_loop()
db = loop.run_until_complete(create_pool())
