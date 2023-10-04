import asyncio
from aiogram import types, Router, F
from aiogram.types import ReplyKeyboardRemove
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command, Filter
from app.database.requests import get_admins, get_users_ids, delete_user
import app.keyboards as kb
import asyncio


router = Router()


class Newsletter(StatesGroup):
    message = State()
    confirmation = State()


class AdminProtect(Filter):
    async def __call__(self, message: types.Message):
        return message.from_user.id in [admin for admin in await get_admins()]


@router.message(AdminProtect(), F.text == '/apanel')
async def check_admin(message: types.Message):
    await message.answer(f'Доступные команды:\n\n/newsletter - Сделать рассылку')


# Рассылка сообщений всем пользователям
@router.message(AdminProtect(), F.text == '/newsletter')
async def newsletter(message: types.Message, state: FSMContext):
    await state.set_state(Newsletter.message)
    await message.answer(f'Внимание! Вы хотите сделать рассылку всем пользователям бота! Введите сообщение ниже. Будьте осторожны, сообщение разошлётся моментально.')


@router.message(AdminProtect(), Newsletter.message)
async def newsletter_message(message: types.Message, state: FSMContext):
    
    await message.answer('Подождите... начинается рассылка. При большом количестве пользователей это может занять время.')
    
    for user_id in await get_users_ids():
        try:
            await message.send_copy(chat_id=user_id)
        except:
            try:
                await delete_user(user_id)
            except:
                continue

    await message.answer('Рассылка завершена!')
