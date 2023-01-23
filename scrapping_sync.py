from typing import List, NoReturn, Tuple
from bs4 import BeautifulSoup, element

def fetch_all_urls(url: str) -> List[Tuple[element.Tag, str]]:
    from urllib.request import urlopen

    args = BeautifulSoup(urlopen(url).read(), 'lxml'),  url
    return scraper.scraping(args)


if __name__ == "__main__":
    import scraper
    import sys, time, pandas as pd

    if sys.version_info[0] != 3 or sys.version_info[1] < 8:
        raise Exception(f'Python Interpreter greater than or equal to version 3.8 is required, your interpreter version is {sys.version_info}' )
    
    all_urls = scraper.get_all_urls()
    start_time = time.perf_counter()
    scrapped_data = [fetch_all_urls(page_url) for page_url in all_urls]
    end_time = time.perf_counter()
    print(f'Total time---------- {end_time - start_time}')

    df = pd.DataFrame(scrapped_data)
    path = r'scrapped_data'
    df.to_csv(f'{path}/sync_sync.csv')
