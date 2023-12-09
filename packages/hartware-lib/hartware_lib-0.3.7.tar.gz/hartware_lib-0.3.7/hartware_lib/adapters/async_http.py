from typing import Dict, Optional

from aiohttp import ClientResponse, ClientSession


class HttpAsyncAdapter:
    def __init__(self, headers: Optional[Dict] = None):
        self.headers = headers or {}

    async def request(
        self, method: str, url: str, extra_headers: Optional[Dict] = None, **kwargs
    ) -> ClientResponse:
        headers = self.headers

        if extra_headers:
            headers.update(extra_headers)

        async with ClientSession() as session:
            response = await session.request(method, url, headers=headers, **kwargs)

            response.raise_for_status()

            return response

    async def get_text(self, *args, **kwargs) -> str:
        response = await self.request(*args, **kwargs)

        return await response.text()

    async def get_json(self, *args, **kwargs) -> Dict:
        response = await self.request(*args, **kwargs)

        return await response.json()
