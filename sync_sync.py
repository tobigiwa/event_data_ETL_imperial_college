from typing import List, NoReturn, Tuple
from bs4 import BeautifulSoup, element

def fetch_all_urls(list_of_url: List[str]) -> List[Tuple[element.Tag, str]]:
    from urllib.request import urlopen

    return [(BeautifulSoup(urlopen(url).read(), 'lxml'), 
                url) 
                for url in list_of_url
                ]


if __name__ == "__main__":
    import scraper
    import sys, time, pandas as pd

    if sys.version_info[0] != 3 or sys.version_info[1] < 8:
        raise Exception(f'Python Interpreter greater than or equal to version 3.8 is required, your interpreter version is {sys.version_info}' )
    
    all_urls = scraper.get_all_urls()
    request_start_time = time.perf_counter()
    htmls = fetch_all_urls(all_urls)
    request_end_time = time.perf_counter()
    scrapped_data = [scraper.scraping(html) for html in htmls]
    parser_end_time = time.perf_counter()

    df = pd.DataFrame(scrapped_data)
    df.to_csv('sync_sync.csv')
    print(f'request time---------- {request_end_time - request_start_time}')
    print(f'parsing time---------- {parser_end_time - request_end_time}')
