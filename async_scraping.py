from typing import List, NoReturn
import asyncio, aiohttp
from bs4 import BeautifulSoup

async def fetch_url(session: aiohttp.ClientSession, url: str,  BeautifulSoup: BeautifulSoup = BeautifulSoup) -> BeautifulSoup:
    async with session.get(url) as response: 
        if response.ok:
            content = await response.text()
            return BeautifulSoup(content, 'lxml')

async def fetch_all(session: aiohttp.ClientSession, list_of_url: List[str]) -> List[BeautifulSoup]:
    tasks = [asyncio.create_task(fetch_url(session, url))
                for url in list_of_url]
    results = await asyncio.gather(*tasks)
    return results

async def main(list_of_url: List[str]) -> NoReturn:
    async with aiohttp.ClientSession() as session:
        htmls = await fetch_all(session, list_of_url)
        titles = [i.title.string for i in htmls]
        print(titles)
            


if __name__ == "__main__":
    import cProfile
    import pstats
    from scraper import get_all_urls

    with cProfile.Profile() as profile:
        all_urls = get_all_urls()
        asyncio.run(main(all_urls))

        results = pstats.Stats(profile)
        results.sort_stats(pstats.SortKey.TIME)
        results.print_stats()



    


