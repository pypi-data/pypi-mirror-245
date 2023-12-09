import json
from typing import AsyncGenerator

import psycopg
import structlog

from ..config import ConfigurationError
from ..sse_starlette import ServerSentEvent

logger = structlog.stdlib.get_logger("brokers.postgres")


class PostgresBroker:
    def __init__(self, postgres_url: str) -> None:
        self.postgres_url = postgres_url
        if not (
            self.postgres_url.startswith("postgres://")
            or self.postgres_url.startswith("postgresql://")
        ):
            raise ConfigurationError("Only PostgreSQL is supported")

    async def listen(self, channel: str) -> AsyncGenerator[ServerSentEvent, None]:
        connection = await psycopg.AsyncConnection.connect(
            self.postgres_url,
            autocommit=True,
        )

        async with connection.cursor() as cursor:
            logger.debug(f"Listening to {channel}")
            await cursor.execute(f"LISTEN {channel}")
            generator = connection.notifies()
            async for notify_message in generator:
                payload = json.loads(notify_message.payload)
                logger.debug(f"Data received from {channel}")
                yield ServerSentEvent(**payload)

    def notify(self, channel: str, sse_payload: dict) -> None:
        connection = psycopg.Connection.connect(
            self.postgres_url,
            autocommit=True,
        )
        logger.debug(f"Publishing to {channel}: {sse_payload}")
        with connection.cursor() as cursor:
            cursor.execute(f"NOTIFY {channel}, '{json.dumps(sse_payload)}'")
