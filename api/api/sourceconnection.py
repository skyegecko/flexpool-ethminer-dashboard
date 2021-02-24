"""
Establish connection to and exchange messages with raw TCP socket which hosts
the source data for this API.
"""
import asyncio
import json
import logging
import os
import random

from typing import Optional

LOGGER = logging.getLogger(__name__)


class Source:
    """
    Class for setting up connections to source data provider
    """

    def __init__(self):
        self.address, _, self.port = os.getenv("APISOURCE").partition(":")
        LOGGER.info("Using connection to %s:%s", self.address, self.port)

    @classmethod
    def generate_id(cls) -> int:
        """
        Generate random integer ID for use in payload.
        """
        return random.randint(0, 5000)

    async def command(self, method: str, params: Optional[dict] = None) -> dict:
        """
        Open a connection to the source on a TCP socket and send `payload` as a
        JSON-encoded string. Await the JSON-encoded response and return that as
        a dict.
        """
        payload = {"id": self.generate_id(), "jsonrpc": "2.0"}
        payload["method"] = method
        if params is not None:
            payload["params"] = params

        json_payload = json.dumps(payload)
        LOGGER.debug("write: %s", json_payload)
        json_payload = json_payload + "\n"

        reader, writer = await asyncio.open_connection(self.address, self.port)

        writer.write(json_payload.encode())
        await writer.drain()

        response_b = await asyncio.wait_for(reader.readline(), timeout=30)
        response = response_b.decode()
        LOGGER.debug("read: %s", response.strip())

        writer.close()
        await writer.wait_closed()

        result = json.loads(response)
        result = {k: v for k, v in result.items() if k not in ("id", "jsonrpc")}

        return result
