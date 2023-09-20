from aiogram import types, Router, F
from aiogram.types import ReplyKeyboardRemove
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command
from app.database.requests import *
import app.keyboards as kb
import asyncio
from app.check_loca import get_address

router = Router()


@router.message(F.text == '/start')
async def cmd_start(message: types.Message):
    await add_user_db(message.from_user.id)
    await message.answer('👋 Добро пожаловать! Отправьте локацию по кнопке ниже ⬇️', reply_markup=kb.main)


@router.message(F.location)
async def location_check(message: types.Message):
    address = await get_address(message.location.latitude, message.location.longitude)
    await message.answer(text=f'🔎 Ваш адрес: {address}. Если это не так, отправьте локацию ещё раз.\n\nБлижайшие точки:', reply_markup=await kb.check(message.location.latitude, message.location.longitude))


@router.message(F.text == '/my_id')
async def my_id(message: types.Message):
    await message.answer(f'Ваш ID: {message.from_user.id}')
