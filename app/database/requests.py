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


async def add_location_db(lat, lon, name):
    async with async_session() as session:
        location_query = await session.scalar(select(Location).where(Location.latitude == lat, Location.longitude == lon))
        
        if not location_query:
            address = await get_address(lat, lon)
            session.add(Location(latitude=lat, longitude=lon, name=name, address=address))
            await session.commit()


async def get_locations():
    async with async_session() as session:
        locations = await session.scalars(select(Location))
        return locations


async def get_location(location_id):
    async with async_session() as session:
        location = await session.scalar(select(Location).where(Location.id == location_id))
        return location


async def get_admins():
    async with async_session() as session:
        admins = await session.scalars(select(Admin.tg_id))
        return admins
