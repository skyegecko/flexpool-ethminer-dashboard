"""
Establish connection to and exchange messages with raw TCP socket which hosts
the source data for this API.
"""
import asyncio
import json
import logging
import random
from typing import NamedTuple, Optional

from api.settings import settings

LOGGER = logging.getLogger(__name__)


class Connection(NamedTuple):
    reader: asyncio.StreamReader
    writer: asyncio.StreamWriter


class Source:
    """
    Class for setting up connections to source data provider
    """

    def __init__(self):
        self.address: str = settings.source_address
        self.port: int = settings.source_port
        self.connection: Connection = None
        self.close_task: asyncio.Task = None

    @classmethod
    def generate_id(cls) -> int:
        """
        Generate random integer ID for use in payload.
        """
        return random.randint(0, 5000)

    async def connect(self) -> None:
        """
        Set up a connection if one doesn't already exist.
        """
        if self.close_task is not None:
            self.close_task.cancel()

        if (
            self.connection is None
            or self.connection.writer.is_closing()
            or self.connection.reader.at_eof()
        ):
            LOGGER.info("Establishing new connection to %s:%s", self.address, self.port)
            self.connection = Connection(
                *(
                    await asyncio.wait_for(
                        asyncio.open_connection(self.address, self.port),
                        timeout=settings.connection_timeout,
                    )
                )
            )

        self.close_task = asyncio.Task(self.sleep_and_close())

    async def sleep_and_close(self) -> None:
        """
        Close the connection after an idle period defined by
        `CONNECTION_KEEPALIVE`.
        """
        await asyncio.sleep(settings.connection_keepalive)

        if self.connection is not None:
            self.connection.writer.close()
            await self.connection.writer.wait_closed()
            LOGGER.info(
                "Connection closed after %s seconds", settings.connection_keepalive
            )

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

        await self.connect()

        json_payload = json.dumps(payload)
        LOGGER.debug("write: %s", json_payload)
        json_payload = json_payload + "\n"

        self.connection.writer.write(json_payload.encode())
        await asyncio.wait_for(
            self.connection.writer.drain(), timeout=settings.connection_timeout
        )

        response_b = await asyncio.wait_for(
            self.connection.reader.readline(), timeout=settings.connection_timeout
        )
        response = response_b.decode()
        LOGGER.debug("read: %s", response.strip())

        result = json.loads(response)
        result = {k: v for k, v in result.items() if k not in ("id", "jsonrpc")}

        return result
