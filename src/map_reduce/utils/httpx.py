import httpx
from asyncio import sleep

__DEFAULT_TIMEOUT_SECONDS: int = 5


class AsyncClient(httpx.AsyncClient):

    async def request(self, *args, **kwargs) -> httpx.Response:
        try:
            response: httpx.Response = await super().request(*args, **kwargs)

            if response.status_code == 429:
                retry_after: int = int(
                    response.headers.get("Retry-After")
                    or __DEFAULT_TIMEOUT_SECONDS
                )
                await sleep(retry_after)
                return await self.request(*args, **kwargs)
        except httpx.ConnectTimeout:
            return await self.request(*args, **kwargs)

        return response
