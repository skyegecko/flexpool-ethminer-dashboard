"""
Entrypoint for FastAPI application
"""
import logging
from typing import Any, Mapping

from fastapi import FastAPI

import api.models.getstatdetail as getstatdetail
from api.models.filtered import Filtered as FilteredModel
from api.models.pong import Pong
from api.settings import settings
from api.sourceconnection import Source

LOGGER = logging.getLogger(__name__)

app = FastAPI(root_path=settings.api_root_path)

source = Source()


@app.get("/", response_model=FilteredModel)
async def root() -> FilteredModel:
    sourceresponse = await source.command("miner_getstatdetail")
    sourcemodel = getstatdetail.Result.parse_obj(sourceresponse)
    return FilteredModel.construct_from_gsd(sourcemodel.result)


@app.get("/ping", response_model=Pong)
async def ping() -> Mapping[str, Any]:
    response = await source.command("miner_ping")
    return response
