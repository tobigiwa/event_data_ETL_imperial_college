from typing import List, NoReturn, Tuple
from bs4 import BeautifulSoup, element

def fetch_all_urls(list_of_url: List[str]) -> List[Tuple[element.Tag, str]]:
    from urllib.request import urlopen

    return [(BeautifulSoup(urlopen(url).read(), 'lxml'), 
                url) 
                for url in list_of_url
                ]


if __name__ == "__main__":
    import sys
    if sys.version_info[0] != 3 or sys.version_info[1] < 8:
        raise Exception(f'Python Interpreter greater than or equal to version 3.8 is required, your interpreter version is {sys.version_info}' )

    import pandas as pd
    import cProfile
    import pstats
    import scraper
    
    with cProfile.Profile() as profile:
        all_urls = scraper.get_all_urls()

        htmls = fetch_all_urls(all_urls)

        scrapped_data = [scraper.scraping(html) for html in htmls]

        df = pd.DataFrame(scrapped_data)
        df.to_csv('sync_data.csv')
        print(df)

        results = pstats.Stats(profile)
        results.sort_stats(pstats.SortKey.TIME)
        results.print_stats()
