from typing import List, NoReturn, Tuple
import asyncio, aiohttp
from bs4 import BeautifulSoup, element
import scraper

def main(url: str) -> List[Tuple[element.Tag, str]]:
    from urllib.request import urlopen

    args = BeautifulSoup(urlopen(url).read(), 'lxml'),  url
    return scraper.scraping(args)


if __name__ == "__main__":
    from scraper import get_all_urls
    import sys, time, pandas as pd
    from concurrent.futures import ProcessPoolExecutor, as_completed

    if sys.version_info[0] != 3 or sys.version_info[1] < 8:
        raise Exception(f'Python Interpreter greater than or equal to version 3.8 is required, your interpreter version is {sys.version_info}' )

    all_urls = get_all_urls()
    with ProcessPoolExecutor() as executor:
        start_time = time.perf_counter()

        futures = [executor.submit(scraper.scraping, all_urls)]
        scrapped_data = [future for future in as_completed(futures)]

        end_time = time.perf_counter()
        print(f'Total time---------- {end_time - start_time}')

        df = pd.DataFrame(scrapped_data)
        path = r'scrapped_data'
        df.to_csv(f'{path}/async_processpool.csv')