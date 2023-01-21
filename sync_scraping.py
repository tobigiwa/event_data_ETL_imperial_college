from typing import List, NoReturn

def main(list_of_url: List[str]) -> NoReturn:
    from urllib.request import urlopen
    from bs4 import BeautifulSoup

    titles = [BeautifulSoup(urlopen(url).read(), 'lxml').title.string for url in list_of_url]
    # print(titles)


if __name__ == "__main__":
    import sys

    if sys.version_info[0] != 3 or sys.version_info[1] < 8:
        raise Exception(f'Python Interpreter greater than or equal to version 3.8 is required, your interpreter version is {sys.version_info}' )

    import cProfile
    import pstats
    from scraper import get_all_urls
    
    with cProfile.Profile() as profile:
        all_urls = get_all_urls()
        main(all_urls)

        results = pstats.Stats(profile)
        results.sort_stats(pstats.SortKey.TIME)
        results.print_stats()
