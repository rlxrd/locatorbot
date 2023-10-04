from app.database.models import async_session
from app.database.models import User, Location, Admin
from sqlalchemy import select, update, delete, desc
from app.check_loca import get_address


async def add_user_db(u_id):
    async with async_session() as session:
        user_query = await session.scalar(select(User).where(User.tg_id == u_id))
        
        if not user_query:
            session.add(User(tg_id=u_id))
            await session.commit()


async def get_locations_device():
    async with async_session() as session:
        locations = await session.scalars(select(Location).where(Location.buy_device == 'X'))
        return locations


async def get_locations_sticks():
    async with async_session() as session:
        locations = await session.scalars(select(Location).where(Location.buy_stick == 'X'))
        return locations


async def get_locations_guarantee():
    async with async_session() as session:
        locations = await session.scalars(select(Location).where(Location.guarantee == 'X'))
        return locations


async def get_locations_international_guarantee():
    async with async_session() as session:
        locations = await session.scalars(select(Location).where(Location.firmware == 'X'))
        return locations


async def get_locations_cleaning():
    async with async_session() as session:
        locations = await session.scalars(select(Location).where(Location.cleaning == 'X'))
        return locations


async def get_location(location_id):
    async with async_session() as session:
        location = await session.scalar(select(Location).where(Location.id == location_id))
        return location


async def get_admins():
    async with async_session() as session:
        admins = await session.scalars(select(Admin.tg_id))
        return admins


async def get_users_ids():
    async with async_session() as session:
        users = await session.scalars(select(User.tg_id))
        return users


async def delete_user(user_id):
    async with async_session() as session:
        await session.execute(delete(User).where(User.tg_id == user_id))
        await session.commit()
