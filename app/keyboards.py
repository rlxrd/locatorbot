from aiogram.types import (InlineKeyboardMarkup, InlineKeyboardButton,
                           ReplyKeyboardMarkup, KeyboardButton, WebAppInfo)
from aiogram.utils.keyboard import InlineKeyboardBuilder
from geopy.distance import geodesic
from app.database.requests import get_locations


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


main = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Отправить локацию', request_location=True)]],
                           resize_keyboard=True,
                           input_field_placeholder='Выберите кнопку ниже')

cancel_kb = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Отмена')]],
                                resize_keyboard=True)


async def check(lat, lon):
    locations = await get_locations()
    keyboard = InlineKeyboardBuilder()
    locations_dict = {}
    for location in locations:
        distance = geodesic((lat, lon), (location.latitude, location.longitude)).meters
        if distance < 5000:
            locations_dict[distance] = location
            
    sorted_dict = {key: locations_dict[key] for key in sorted(locations_dict)}
    
    for dist, location in sorted_dict.items():
        keyboard.row(InlineKeyboardButton(text=f'{round(dist)}м - {location.name[:25]}', web_app=WebAppInfo(url=generate_yandex_maps_link(location.latitude, location.longitude, location.name))))
    return keyboard.as_markup()
