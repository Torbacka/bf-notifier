from aiohttp import ClientSession, TCPConnector
from pypeln import asyncio_task as aio

from html_parser import parser

limit = 1000
urls = map(lambda x: f"https://bostad.stockholm.se/Lista/Details/?aid={x + 153292}", range(10))


async def fetch(url, session):
    async with session.get(url) as response:
        response = await response.read()
        ad = parser.parse_ad_page(dict(), url, response)
        print(ad)
        return response


aio.each(
    fetch,
    urls,
    workers=limit,
    on_start=lambda: ClientSession(connector=TCPConnector(limit=None)),
    on_done=lambda _status, session: session.close(),
    run=True,
)
