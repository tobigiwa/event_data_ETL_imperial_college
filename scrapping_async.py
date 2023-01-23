from typing import List, NoReturn, Tuple
import asyncio, aiohttp
from bs4 import BeautifulSoup, element
import scraper


async def fetch_url(session: aiohttp.ClientSession, url: str,  BeautifulSoup: element.Tag = BeautifulSoup) -> Tuple[element.Tag, str]:
    async with session.get(url) as response: 
        if response.ok:
            content = await response.text()
            args = BeautifulSoup(content, 'lxml'), url
            return scraper.scraping(args)

async def fetch_all_urls(session: aiohttp.ClientSession, list_of_url: List[str]) -> List[Tuple[element.Tag, str]]:
    tasks = [asyncio.create_task(fetch_url(session, url))
                for url in list_of_url]
    results = await asyncio.gather(*tasks)
    return results


async def main(list_of_url: List[str]) -> NoReturn:
    import pandas as pd
    import time

    async with aiohttp.ClientSession() as session:
        start_time = time.perf_counter()
        scrapped_data = await fetch_all_urls(session, list_of_url)
        end_time = time.perf_counter()
        print(f'Total time---------- {end_time - start_time}')

        df = pd.DataFrame(scrapped_data)
        path = r'scrapped_data'
        df.to_csv(f'{path}/async.csv')


if __name__ == "__main__":
    from scraper import get_all_urls
    import sys

    if sys.version_info[0] != 3 or sys.version_info[1] < 8:
        raise Exception(f'Python Interpreter greater than or equal to version 3.8 is required, your interpreter version is {sys.version_info}' )

    all_urls = get_all_urls()
    asyncio.run(main(all_urls))