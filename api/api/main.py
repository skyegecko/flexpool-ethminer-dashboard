import logging

from fastapi import FastAPI

from api.sourceconnection import Source


LOGGER = logging.getLogger(__name__)

app = FastAPI()

source = Source()


@app.get("/")
async def root():
    LOGGER.info("hello")
    return {"message": "Hello World!"}


@app.get("/ping")
async def ping():
    LOGGER.debug("ping")
    response = await source.command("miner_ping")
    LOGGER.debug("pong")
    return response
