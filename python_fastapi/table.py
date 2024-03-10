from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import mapped_column
from sqlalchemy import Integer, String

from db import db


class Base(DeclarativeBase):
    __abstract__ = True


class Test(Base):
    __tablename__ = "test"

    id = mapped_column(Integer, primary_key=True)
    data = mapped_column(String(50), nullable=False)
