from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Column, Integer, String, ARRAY, Float, ForeignKey, Date
from sqlalchemy.orm import relationship

class Base(DeclarativeBase):
    pass

