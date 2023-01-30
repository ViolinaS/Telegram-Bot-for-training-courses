from aiogram import types, Bot
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

bot = Bot(token=os.getenv('Token'))
dp = Dispatcher(bot)

@dp.message_handler(commands='/start')
async def start(message: types.Message):
    await message.answer('Hello')
    


executor.start_polling(dp, skip_updates=True)