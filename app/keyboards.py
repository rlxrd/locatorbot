from aiogram.types import (InlineKeyboardMarkup, InlineKeyboardButton,
                           ReplyKeyboardMarkup, KeyboardButton, WebAppInfo)
from aiogram.utils.keyboard import InlineKeyboardBuilder
from geopy.distance import geodesic
from app.database.requests import (get_locations_device, get_locations_sticks,
                                   get_locations_guarantee, get_locations_international_guarantee,
                                   get_locations_cleaning)


def generate_yandex_maps_link(latitude, longitude, point_name):
    base_url = "https://yandex.ru/maps"
    query_parameters = {
        "ll": f"{longitude},{latitude}",
        "z": "17",  # Уровень масштабирования (от 1 до 19)
        "l": "map",  # Тип карты: "map" - обычная карта, "sat" - спутниковая карта, "skl" - гибрид
        "pt": f"{longitude},{latitude}"
    }
    encoded_parameters = "&".join([f"{key}={value}" for key, value in query_parameters.items()])
    yandex_maps_link = f"{base_url}?{encoded_parameters}"
    return yandex_maps_link


menu = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Покупка девайса', callback_data='buy_device')],
    [InlineKeyboardButton(text='Покупка стиков', callback_data='buy_sticks')],
    [InlineKeyboardButton(text='Service', callback_data='service')]
])

service = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Гарантийная замена', callback_data='guarantee')],
    [InlineKeyboardButton(text='Международная гарантия/Прошивка', callback_data='international_guarantee')],
    [InlineKeyboardButton(text='Чистка', callback_data='cleaning')]
])

main = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='📍 Отправить локацию', request_location=True)]],
                           resize_keyboard=True,
                           input_field_placeholder='Выберите кнопку ниже ⬇️')

cancel_kb = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Отмена')]],
                                resize_keyboard=True)


async def check(lat, lon, type):
    
    if type == 'buy_device':
        locations = await get_locations_device()
        my_distance = 1000
    elif type == 'buy_sticks':
        locations = await get_locations_sticks()
        my_distance = 1000
    elif type == 'guarantee':
        locations = await get_locations_guarantee()
        my_distance = 10000
    elif type == 'international_guarantee':
        locations = await get_locations_international_guarantee()
        my_distance = 10000
    elif type == 'cleaning':
        locations = await get_locations_cleaning()
        my_distance = 10000
    
    keyboard = InlineKeyboardBuilder()
    locations_dict = {}
    
    for location in locations:
        distance = geodesic((lat, lon), (location.latitude, location.longitude)).meters
        if distance < my_distance:
            locations_dict[distance] = location
            
    sorted_dict = {key: locations_dict[key] for key in sorted(locations_dict)}
    
    if len(sorted_dict.keys()) >= 1:
        for dist, location in sorted_dict.items():
            keyboard.row(InlineKeyboardButton(text=f'{round(dist)}м - {location.name[:25]}', callback_data=f'location_{location.id}', web_app=WebAppInfo(url=generate_yandex_maps_link(location.latitude, location.longitude, location.name))))
        keyboard.row(InlineKeyboardButton(text='🏠 В главное меню', callback_data='main_menu'))
        return keyboard.as_markup()
    else:
        return None


async def open_location(location):
    keyboard = InlineKeyboardBuilder()
    keyboard.row(InlineKeyboardButton(text='🗾 Открыть на картах', web_app=WebAppInfo(url=generate_yandex_maps_link(location.latitude, location.longitude, location.name))))
    keyboard.row(InlineKeyboardButton(text='✍🏻 Оставить отзыв', callback_data=f'feedback_{location.id}'))
    keyboard.row(InlineKeyboardButton(text='🏠 В главное меню', callback_data='main_menu'))
    return keyboard.as_markup()


done = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Готово ✅')]],
                           resize_keyboard=True)
