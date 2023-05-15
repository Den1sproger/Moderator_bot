import os

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from dotenv import load_dotenv, find_dotenv


load_dotenv(find_dotenv())

TOKEN = os.getenv('MODERATOR_TOKEN')
ADMIN = int(os.getenv('ADMIN'))
USERS_FILE_PATH = 'handlers/users.json'
bot = Bot(TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())
