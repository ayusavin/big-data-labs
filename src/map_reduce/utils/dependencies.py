from contextlib import asynccontextmanager
from typing import AsyncGenerator

from .httpx import AsyncClient


@asynccontextmanager
async def http_client_factory(
    base_url: str = ""
) -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(base_url=base_url) as client:
        yield client
