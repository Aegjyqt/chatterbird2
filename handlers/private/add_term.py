from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
import datetime

import database.database_sql
from main import dp


class AddTermPipeline(StatesGroup):
    add_term_ru = State()
    add_term_en = State()
    add_term_comment = State()


@dp.message_handler(commands=['add_term'])
async def init_add_term(message: types.Message) -> None:
    await message.answer(text='Enter term in RU:')
    await AddTermPipeline.add_term_ru.set()


@dp.message_handler(state=AddTermPipeline.add_term_ru)
async def record_term_ru(message: types.Message, state: FSMContext) -> None:
    async with state.proxy() as data:
        data['term_ru'] = message.text
    await message.answer(text='Enter term in EN:')
    await AddTermPipeline.add_term_en.set()


@dp.message_handler(state=AddTermPipeline.add_term_en)
async def record_term_ru(message: types.Message, state: FSMContext) -> None:
    async with state.proxy() as data:
        data['term_en'] = message.text
    await message.answer(text='Enter your comments:')
    await AddTermPipeline.add_term_comment.set()


@dp.message_handler(state=AddTermPipeline.add_term_comment)
async def record_term_ru(message: types.Message, state: FSMContext) -> None:
    async with state.proxy() as data:
        data['term_comments'] = message.text
        data['added_by'] = message.from_user.id
        data['added_on'] = datetime.datetime.now()
        with database.database_sql.BotDb() as db:
            db.add_term(term_ru=data['term_ru'], term_en=data['term_en'], comments=data['term_comments'],
                        added_by=data['added_by'], added_on=data['added_on'])
    await message.answer(text='Term added!')
    await state.finish()
