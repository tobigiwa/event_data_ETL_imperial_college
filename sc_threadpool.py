from typing import List, Tuple
from bs4 import BeautifulSoup, element
import scrapper

def fetch_all_urls(url: str) -> List[Tuple[element.Tag, str]]:
    from urllib.request import urlopen

    args = BeautifulSoup(urlopen(url).read(), 'lxml'),  url
    return scrapper.main(args)


if __name__ == "__main__":
    import sys, time, pandas as pd
    from concurrent.futures import ThreadPoolExecutor, as_completed

    if sys.version_info[0] != 3 or sys.version_info[1] < 8:
        raise Exception(f'Python Interpreter greater than or equal to version 3.8 is required, your interpreter version is {sys.version_info}' )

    all_urls = scrapper.get_all_urls()
    with ThreadPoolExecutor() as executor:
        start_time = time.perf_counter()

        futures = [executor.submit(fetch_all_urls, page_url) for page_url in all_urls]
        scrapped_data = [future.result() for future in as_completed(futures)]

        end_time = time.perf_counter()
        print(f'----------Total time---- with ThreadPoolExecutor----------- {end_time - start_time}')

        df = pd.DataFrame(scrapped_data)
        path = r'scrapped_data'
        df.to_csv(f'{path}/threadpool.csv')

__all__ = []