from aiogram import types, Router, F, Bot
from aiogram.types import ReplyKeyboardRemove
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command
from app.database.requests import add_user_db, get_location
import app.keyboards as kb
import asyncio
from app.check_loca import get_address

router = Router()


class Categories(StatesGroup):
    device = State()
    stick = State()
    guarantee = State()
    firmware = State()
    cleaning = State()


class Feedback(StatesGroup):
    feedback = State()


# Начальные команды
@router.message(F.text == '/start')
async def cmd_start(message: types.Message):
    await add_user_db(message.from_user.id)
    await message.answer('👋 Добро пожаловать! Выберите пункт ниже ⬇️', reply_markup=kb.menu)


@router.callback_query(F.data == 'service')
async def cmd_service(call: types.CallbackQuery):
    await call.message.edit_text('⚙️ Выберите интересующий вас вариант Service.', reply_markup=kb.service)


# Покупка девайса
@router.callback_query(F.data == 'buy_device')
async def cmd_buy_device(call: types.CallbackQuery, state: FSMContext):
    await state.set_state(Categories.device)
    await call.answer('📍 Вы выбрали покупку девайса.')
    await call.message.answer('📍 Для того, чтобы найти ближайшие точки продаж девайсов, отправьте локацию по кнопке ниже.',
                              reply_markup=kb.main)


@router.message(Categories.device, F.location)
async def location_check_device(message: types.Message, state: FSMContext, bot: Bot):
    
    message_id = await message.answer('Поиск...', reply_markup=ReplyKeyboardRemove())
    
    address = await get_address(message.location.latitude, message.location.longitude)
    keyboard = await kb.check(message.location.latitude, message.location.longitude, 'buy_device')
    
    await bot.delete_message(chat_id=message.from_user.id, message_id=message_id.message_id)
    
    if not keyboard:
        await message.answer(f'🔎 Ваш адрес: {address}.\n\nК сожалению, вблизи точек нет.', reply_markup=ReplyKeyboardRemove())
        await message.answer('Выберите пункт ниже ⬇️', reply_markup=kb.menu)
    else:
        await message.answer(text=f'🔎 Ваш адрес: {address}. Если это не так, отправьте локацию ещё раз.\n\nБлижайшие точки для покупки девайса:',
                            reply_markup=keyboard)
    await state.clear()
    

# Покупка стиков
@router.callback_query(F.data == 'buy_sticks')
async def cmd_buy_sticks(call: types.CallbackQuery, state: FSMContext):
    await state.set_state(Categories.stick)
    await call.answer('📍 Вы выбрали покупку стиков.')
    await call.message.answer('📍 Для того, чтобы найти ближайшие точки продаж стиков, отправьте локацию по кнопке ниже.',
                              reply_markup=kb.main)


@router.message(Categories.stick, F.location)
async def location_check_sticks(message: types.Message, state: FSMContext, bot: Bot):
    
    message_id = await message.answer('Поиск...', reply_markup=ReplyKeyboardRemove())

    address = await get_address(message.location.latitude, message.location.longitude)
    keyboard = await kb.check(message.location.latitude, message.location.longitude, 'buy_sticks')
    
    await bot.delete_message(chat_id=message.from_user.id, message_id=message_id.message_id)
    
    if not keyboard:
        await message.answer(f'🔎 Ваш адрес: {address}.\n\nК сожалению, вблизи точек нет.', reply_markup=ReplyKeyboardRemove())
        await message.answer('Выберите пункт ниже ⬇️', reply_markup=kb.menu)
    else:
        await message.answer(text=f'🔎 Ваш адрес: {address}. Если это не так, отправьте локацию ещё раз.\n\nБлижайшие точки для покупки стиков:',
                            reply_markup=keyboard)
    await state.clear()


# Гарантийная замена
@router.callback_query(F.data == 'guarantee')
async def cmd_buy_sticks(call: types.CallbackQuery, state: FSMContext):
    await state.set_state(Categories.guarantee)
    await call.answer('📍 Вы выбрали гарантийную замену.')
    await call.message.answer('📍 Для того, чтобы найти ближайшие точки гарантийной замены, отправьте локацию по кнопке ниже.',
                              reply_markup=kb.main)


@router.message(Categories.guarantee, F.location)
async def location_check_sticks(message: types.Message, state: FSMContext, bot: Bot):
    
    message_id = await message.answer('Поиск...', reply_markup=ReplyKeyboardRemove())
    
    address = await get_address(message.location.latitude, message.location.longitude)
    keyboard = await kb.check(message.location.latitude, message.location.longitude, 'guarantee')
    
    await bot.delete_message(chat_id=message.from_user.id, message_id=message_id.message_id)
    
    if not keyboard:
        await message.answer(f'🔎 Ваш адрес: {address}.\n\nК сожалению, вблизи точек нет.', reply_markup=ReplyKeyboardRemove())
        await message.answer('Выберите пункт ниже ⬇️', reply_markup=kb.menu)
    else:
        await message.answer(text=f'🔎 Ваш адрес: {address}. Если это не так, отправьте локацию ещё раз.\n\nБлижайшие точки для гарантийной замены:',
                            reply_markup=await kb.check(message.location.latitude, message.location.longitude, 'guarantee'))
    await state.clear()


# Международная замена/прошивка
@router.callback_query(F.data == 'international_guarantee')
async def cmd_buy_sticks(call: types.CallbackQuery, state: FSMContext):
    await state.set_state(Categories.firmware)
    await call.answer('📍 Вы выбрали международную замену/Прошивку.')
    await call.message.answer('📍 Для того, чтобы найти ближайшие точки международной замены/Прошивки, отправьте локацию по кнопке ниже.',
                              reply_markup=kb.main)


@router.message(Categories.firmware, F.location)
async def location_check_sticks(message: types.Message, state: FSMContext, bot: Bot):
    
    message_id = await message.answer('Поиск...', reply_markup=ReplyKeyboardRemove())

    address = await get_address(message.location.latitude, message.location.longitude)
    keyboard = await kb.check(message.location.latitude, message.location.longitude, 'international_guarantee')
    
    await bot.delete_message(chat_id=message.from_user.id, message_id=message_id.message_id)
    
    if not keyboard:
        await message.answer(f'🔎 Ваш адрес: {address}.\n\nК сожалению, вблизи точек нет.', reply_markup=ReplyKeyboardRemove())
        await message.answer('Выберите пункт ниже ⬇️', reply_markup=kb.menu)
    else:
        await message.answer(text=f'🔎 Ваш адрес: {address}. Если это не так, отправьте локацию ещё раз.\n\nБлижайшие точки для международной замены/Прошивки:',
                             reply_markup=keyboard)
    await state.clear()


# Очистка
@router.callback_query(F.data == 'cleaning')
async def cmd_buy_sticks(call: types.CallbackQuery, state: FSMContext):
    await state.set_state(Categories.cleaning)
    await call.answer('📍 Вы выбрали чистку.')
    await call.message.answer('📍 Для того, чтобы найти ближайшие точки чистки, отправьте локацию по кнопке ниже.',
                              reply_markup=kb.main)


@router.message(Categories.cleaning, F.location)
async def location_check_sticks(message: types.Message, state: FSMContext, bot: Bot):
    
    message_id = await message.answer('Поиск...', reply_markup=ReplyKeyboardRemove())

    address = await get_address(message.location.latitude, message.location.longitude)
    keyboard = await kb.check(message.location.latitude, message.location.longitude, 'cleaning')
    
    await bot.delete_message(chat_id=message.from_user.id, message_id=message_id.message_id)
    
    if not keyboard:
        await message.answer(f'🔎 Ваш адрес: {address}.\n\nК сожалению, вблизи точек нет.', reply_markup=ReplyKeyboardRemove())
        await message.answer('Выберите пункт ниже ⬇️', reply_markup=kb.menu)
    else:
        await message.answer(text=f'🔎 Ваш адрес: {address}. Если это не так, отправьте локацию ещё раз.\n\nБлижайшие точки для чистки:',
                            reply_markup=keyboard)
    await state.clear()


# Сама локация с кнопками
@router.callback_query(F.data.startswith('location_'))
async def location(callback: types.CallbackQuery):
    location_id = callback.data.split('_')[1]
    location = await get_location(location_id)
    await callback.answer()
    await callback.message.answer(f'Вы выбрали {location.name}. Вы можете открыть эту точку на картах или оставить отзыв!', reply_markup=await kb.open_location(location))


# Отправка фидбека
@router.callback_query(F.data.startswith('feedback_'))
async def location_feedback(callback: types.CallbackQuery, state: FSMContext):
    location_id = callback.data.split('_')[1]
    location = await get_location(location_id)
    await state.update_data(location_name=location.name, location_lat=location.latitude, location_lon=location.longitude)
    await callback.answer()
    await state.set_state(Feedback.feedback)
    await callback.message.answer('Оставьте отзыв в виде текста/фото/видео и нажмите кнопку готово ✅.', reply_markup=kb.done)


# Фидбек отправлен
@router.message(Feedback.feedback, F.text == 'Готово ✅')
async def feedback_done(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer('Спасибо за отзыв!', reply_markup=ReplyKeyboardRemove())
    await message.answer('Выберите пункт ниже ⬇️', reply_markup=kb.menu)
    

# Пересылка в группу
@router.message(Feedback.feedback)
async def feedback(message: types.Message, state: FSMContext, bot: Bot):
    location_data = await state.get_data()
    #await message.send_copy(chat_id=-4024079069)
    await bot.send_message(chat_id=-1001941830316, text=f'Отзыв о: {location_data["location_name"]}.\n{location_data["location_lat"]}, {location_data["location_lon"]}')
    await message.send_copy(chat_id=-1001941830316)


@router.message(F.text == '/my_id')
async def my_id(message: types.Message):
    await message.answer(f'{message.from_user.id}')


@router.callback_query(F.data == 'main_menu')
async def main_menu(callback: types.CallbackQuery):
    await callback.answer('Вы вернулись в главное меню.')
    await callback.message.edit_text('Выберите пункт ниже ⬇️', reply_markup=kb.menu)


@router.message(F.location)
async def del_loca(message: types.Message):
    await message.answer('Выберите пункт из меню или перезапустите бота.', reply_markup=ReplyKeyboardRemove())
    await message.delete()