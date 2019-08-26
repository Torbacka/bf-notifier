from aiohttp import ClientSession, TCPConnector
from pypeln import asyncio_task as aio

from database.ad_dao import insert_ad
from html_parser import parser

limit = 1000
urls = map(lambda x: f"https://bostad.stockholm.se/Lista/Details/?aid={x +1000}", range(1000))


async def fetch(url, session):
    async with session.get(url) as response:
        if response.status is not 200:
            return response
        response = await response.read()
        ad = parser.parse_ad_page(dict(), url, response)
        if ad is not None:
            insert_ad(ad)
        return response


aio.each(
    fetch,
    urls,
    workers=limit,
    on_start=lambda: ClientSession(connector=TCPConnector(limit=None)),
    on_done=lambda _status, session: session.close(),
    run=True,
)
