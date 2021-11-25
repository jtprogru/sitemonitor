"""Http client module."""

from aiohttp import ClientResponse, ClientSession, ClientTimeout


class HttpClient:
    @staticmethod
    async def request(method: str, url: str, timeout: int) -> ClientResponse:
        async with ClientSession(timeout=ClientTimeout(timeout)) as session:
            async with session.request(method, url) as response:
                return response
