import asyncio
import logging
import os

from aiogram import Dispatcher, Bot
from database.connection import flush_db, engine

from handlers.start import router

TOKEN =  "7590259293:AAH0g6z1cni6jDJxgJjn6WSXigB8RpvvzGI"

bot = Bot(token=TOKEN)
dp = Dispatcher()

async def db_startup(dispatcher: Dispatcher):
    await flush_db(engine=engine)

async def main():
    dp.include_router(router)
    await db_startup(dp)
    await dp.start_polling(bot)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('exit')
