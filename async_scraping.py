from typing import List, NoReturn, Tuple
import asyncio, aiohttp
from bs4 import BeautifulSoup
import scraper

async def fetch_url(session: aiohttp.ClientSession, url: str,  BeautifulSoup: BeautifulSoup = BeautifulSoup) -> Tuple[BeautifulSoup, str]:
    async with session.get(url) as response: 
        if response.ok:
            content = await response.text()
            return BeautifulSoup(content, 'lxml'), url


async def fetch_all_urls(session: aiohttp.ClientSession, list_of_url: List[str]) -> List[Tuple[BeautifulSoup, str]]:
    tasks = [asyncio.create_task(fetch_url(session, url))
                for url in list_of_url]
    results = await asyncio.gather(*tasks)
    return results


async def main(list_of_url: List[str]) -> NoReturn:
    import pandas as pd

    async with aiohttp.ClientSession() as session:
        htmls = await fetch_all_urls(session, list_of_url)
        scrapped_data = [scraper.scraping(html) for html in htmls]
        df = pd.DataFrame(scrapped_data)
        df.to_csv('async_data.csv')

if __name__ == "__main__":
    import sys
    if sys.version_info[0] != 3 or sys.version_info[1] < 8:
        raise Exception(f'Python Interpreter greater than or equal to version 3.8 is required, your interpreter version is {sys.version_info}' )

    import cProfile
    import pstats
    from scraper import get_all_urls

    with cProfile.Profile() as profile:
        all_urls = get_all_urls()
        asyncio.run(main(all_urls))

        results = pstats.Stats(profile)
        results.sort_stats(pstats.SortKey.TIME)
        results.print_stats()



    


