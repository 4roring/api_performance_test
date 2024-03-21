import os
from asyncio import current_task
from typing import Annotated, AsyncIterator
from fastapi import Depends
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session, Session
from sqlalchemy.exc import SQLAlchemyError

from sqlalchemy.ext.asyncio import (
    async_sessionmaker,
    create_async_engine,
    async_scoped_session,
    AsyncSession,
)


class Database:
    def __init__(self):
        self.engine = create_engine(
            "mysql+pymysql://root:root@localhost:3306/profile",
            pool_pre_ping=True,
        )
        self.session_factory = sessionmaker(
            bind=self.engine, autoflush=False, autocommit=False
        )
        self.scoped_session = scoped_session(self.session_factory)

        self.async_engine = create_async_engine(
            "mysql+aiomysql://root:root@localhost:3306/profile",
            pool_pre_ping=True,
        )
        self.async_session_factory = async_sessionmaker(
            bind=self.async_engine,
            autoflush=False,
            future=True,
        )
        self.async_scoped_session = async_scoped_session(
            self.async_session_factory, scopefunc=current_task
        )

    async def get_session(self) -> AsyncIterator[AsyncSession]:
        async with self.async_scoped_session() as session:
            try:
                yield session
                await session.commit()
            except SQLAlchemyError as e:
                await session.rollback()
            finally:
                await session.close()

    def get_sync_session(self) -> Session:
        sync_db = self.scoped_session()
        try:
            yield sync_db
        finally:
            sync_db.close()


db = Database()
AsyncSessionDepends = Annotated[AsyncSession, Depends(db.get_session)]
SessionDepends = Annotated[Session, Depends(db.get_sync_session)]
