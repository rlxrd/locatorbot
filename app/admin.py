import asyncio
from aiogram import types, Router, F
from aiogram.types import ReplyKeyboardRemove
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command, Filter
from app.database.requests import *
import app.keyboards as kb
import asyncio


router = Router()
ADMINS = [123]

class AddLocation(StatesGroup):
    lat = State()
    lon = State()
    name = State()


class AdminProtect(Filter):
    """
    Фильтр для проверки пользователя на админа
    """
    def __init__(self):
        self.admins = ADMINS

    async def __call__(self, message: types.Message):
        return message.from_user.id in self.admins


@router.message(AdminProtect(), F.text == '/add_location')
async def add_cmd(message: types.Message, state: FSMContext):
    await state.set_state(AddLocation.lat)
    await message.answer('Введите latitude (первое число)', reply_markup=kb.cancel_kb)


@router.message(AddLocation.lat)
async def add_lat(message: types.Message, state: FSMContext):
    await state.update_data(lat=message.text)
    await state.set_state(AddLocation.lon)
    await message.answer('Введите longitude (второе число)', reply_markup=kb.cancel_kb)


@router.message(AddLocation.lon)
async def add_lon(message: types.Message, state: FSMContext):
    await state.update_data(lon=message.text)
    await state.set_state(AddLocation.name)
    await message.answer('Введите название точки. Например ТЦ Atlas, Чиланзар', reply_markup=kb.cancel_kb)
    
    
@router.message(AddLocation.name)
async def add_lon(message: types.Message, state: FSMContext):
    try:
        await state.update_data(name=message.text)
        data = await state.get_data()
        await add_location_db(data['lat'], data['lon'], data['name'])
        await state.clear()
        await message.answer('Готово', reply_markup=kb.main)
    except Exception as err:
        await message.answer(f'Ошибка: {err}')

