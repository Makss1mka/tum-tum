from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from ..models.entities import Book, Base
from dotenv import load_dotenv
import os

load_dotenv()

username = os.environ.get("DB_USERNAME")
password = os.environ.get("DB_PASSWORD")
bd_name = os.environ.get("DB_NAME")
host = os.environ.get("DB_HOST")
url = os.environ.get("DB_URL")

engine = None
AsyncSessionMaker = None

if (url != None and username != None and password != None and bd_name != None and host != None):
    engine = create_async_engine(url.format(username=username, password=password, host=host, bd_name=bd_name))
    AsyncSessionMaker = sessionmaker(engine, class_=AsyncSession)


