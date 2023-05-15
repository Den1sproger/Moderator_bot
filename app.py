from aiogram import executor
from bot_config import dp
from handlers.main import *


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
