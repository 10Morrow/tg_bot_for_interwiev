# -*- coding: utf-8 -*-
import asyncio
import asyncpg
import logging
from data import config

logger = logging.getLogger('app.sql')


async def create_db():
    create_db_command = open("database/create_database.sql", "r").read()

    logger.info("Connecting to database...")
    conn: asyncpg.Connection = await asyncpg.connect(user=config.user,
                                     password=config.password,
                                     host=config.host,
                                     port=config.port)
    await conn.execute(create_db_command)
    await conn.close()
    logger.info("Table users created")
    print('подключились')

async def create_pool():
    return await asyncpg.create_pool(user=config.user,
                                     password=config.password,
                                     host=config.host)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(create_db())