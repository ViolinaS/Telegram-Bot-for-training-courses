from aiogram import Bot
from aiogram.dispatcher import Dispatcher
import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())
bot = Bot(token=os.getenv('Token'))
dp = Dispatcher(bot)
