from fastapi import FastAPI
import time
import asyncio

app = FastAPI()


@app.get("/async")
async def read_root():
    while True:
        time.sleep(10)

    return {"Hello": "World"}


@app.get("/sync")
def read_root():
    while True:
        time.sleep(1)

    return {"Hello": "World"}


@app.get("/")
def read_root():
    return {"Hello": "World"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app)
