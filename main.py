from aiogram import Bot, Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from dotenv import load_dotenv
import os


load_dotenv()

bot = Bot(
          token=os.getenv('TOKEN'),
          parse_mode='HTML'
          )

dp = Dispatcher(bot=bot, storage=MemoryStorage())


if __name__ == "__main__":
    from handlers import dp
    executor.start_polling(dp)
