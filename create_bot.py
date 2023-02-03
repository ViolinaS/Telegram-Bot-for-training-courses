from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

storage = MemoryStorage()

bot = Bot(token=os.getenv('Token'))
dp = Dispatcher(bot, storage=storage)

bot_address = os.getenv('bot_name')

master_id = os.getenv('master_id_owner')