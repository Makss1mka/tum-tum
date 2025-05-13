from globals import DB_USERNAME, DB_HOST, DB_NAME, DB_PASSWORD, DB_URL
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from models import entities

engine = None
AsyncSessionMaker = None

if (DB_URL != None 
    and DB_USERNAME != None 
    and DB_PASSWORD != None 
    and DB_NAME != None 
    and DB_HOST != None
):
    engine = create_async_engine(
        DB_URL.format(
            username=DB_USERNAME,
            password=DB_PASSWORD,
            host=DB_HOST,
            bd_name=DB_NAME
        )
    )
    AsyncSessionMaker = sessionmaker(engine, class_=AsyncSession)


