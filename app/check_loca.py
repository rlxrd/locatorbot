from geopy.geocoders import Nominatim


async def get_address(latitude, longitude, lang='ru'):
    geolocator = Nominatim(user_agent="TelegramBotForShop")
    location = geolocator.reverse(f"{latitude}, {longitude}", exactly_one=True, language=lang)
    if location:
        return location.address
    else:
        return "Адрес не найден"
