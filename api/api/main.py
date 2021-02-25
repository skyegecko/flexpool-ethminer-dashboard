import logging

from fastapi import FastAPI

from api.settings import settings
from api.sourceconnection import Source


LOGGER = logging.getLogger(__name__)

app = FastAPI(root_path=settings.api_root_path)

source = Source()


@app.get("/")
async def root():
    LOGGER.info("hello")
    return {"message": "Hello World!"}


@app.get("/ping")
async def ping():
    response = await source.command("miner_ping")
    return response


@app.get("/stats")
async def stats():
    result = await source.command("miner_getstat1")
    result = result["result"]
    response = {}
    response["version"] = result[0]
    response["uptime_minutes"] = result[1]
    (
        response["hashrate_khs"],
        response["submitted_shares"],
        response["rejected_shares"],
    ) = result[2].split(";")
    response["hashrate_per_gpu_khs"] = result[3].split(";")
    response["temps_per_gpu_c"] = result[6].split(";")[0::2]
    response["fanspeeds_per_gpu_percent"] = result[6].split(";")[1::2]
    response["current_pool"] = result[7]
    return response


@app.get("/detailedstats")
async def detailedstats():
    response = await source.command("miner_getstatdetail")
    return response


@app.get("/connections")
async def connections():
    response = await source.command("miner_getconnections")
    return response
