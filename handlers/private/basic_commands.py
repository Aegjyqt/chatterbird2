import datetime
from aiogram import types
from aiogram.dispatcher import FSMContext

import database.database_sql
import elements.messages

from main import dp


@dp.message_handler(commands=['start'])
async def welcome_and_register(message: types.Message) -> None:
    with database.database_sql.BotDb() as db:
        db.add_user(user_id=message.from_user.id,
                    user_name=f'{message.from_user.first_name} {message.from_user.last_name}',
                    reg_time=str(datetime.datetime.now()), is_admin=False)
        await message.answer(text=elements.messages.welcome)


@dp.message_handler(commands=['about'])
async def about(message: types.Message) -> None:
    await message.answer(text=elements.messages.about)


@dp.message_handler(commands=['cancel'], state='*')
async def cancel(message: types.Message, state: FSMContext) -> None:
    await message.answer(text=f'{state} cancelled')
    await state.finish()

