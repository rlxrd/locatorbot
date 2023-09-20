import asyncio
import logging
from config import TOKEN

from app.database.models import async_main
from aiogram import Bot, Dispatcher

from app.handlers import router
from app.admin import router as admin


# Main func for start DB/polling
async def main():
    await async_main()  # Start DB

    bot = Bot(token=TOKEN, parse_mode='HTML')
    dp = Dispatcher()
    dp.include_routers(router, admin)  # Routers
    
    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)  # Logging
    try:
        asyncio.get_event_loop().run_until_complete(main())
    except KeyboardInterrupt:  # Listen Ctrl + C
        print('Exit')
