from fastapi import FastAPI
import time
import asyncio
from sqlalchemy import select, insert, delete
from table import Base, Test
from db import AsyncSessionDepends, SessionDepends, db

app = FastAPI()

Base.metadata.drop_all(db.engine)
Base.metadata.create_all(db.engine)


@app.get("/async/select")
async def select_async(session: AsyncSessionDepends):
    stmt = select(Test)
    result = await session.execute(stmt)
    data = result.scalars()
    return {"data": data.all()}


@app.post("/async/insert/{value}")
async def insert_async(session: AsyncSessionDepends, value: str):
    test = Test(data=value)
    session.add(test)
    await session.flush()
    return "success"


@app.post("/async/delete/{value}")
async def delete_async(session: AsyncSessionDepends, value: str):
    stmt = delete(Test).where(Test.data == value)
    await session.execute(stmt)
    return "success"


@app.get("/sync/select")
def select_sync(session: SessionDepends):
    stmt = select(Test)
    result = session.execute(stmt)
    data = result.scalars()
    return {"data": data.all()}


@app.post("/sync/insert/{value}")
def insert_sync(session: SessionDepends, value: str):
    test = Test(data=value)
    session.add(test)
    return "success"


@app.post("/sync/delete/{value}")
def delete_sync(session: SessionDepends, value: str):
    stmt = delete(Test).where(Test.data == value)
    session.execute(stmt)
    return "success"


@app.get("/")
def read_root():
    return {"Hello": "World"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app)
