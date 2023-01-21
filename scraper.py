from bs4 import BeautifulSoup
from typing import List

large_num: int = 1000
start_url: str = f"https://www.imperial.ac.uk/whats-on/?audience=&match=any&quantity={large_num}&show=future&start=0&tags=institutional-event"

def get_all_urls(url: str = start_url, BeautifulSoup: BeautifulSoup = BeautifulSoup) -> List[str]:
    from urllib.request import urlopen
    from urllib.parse import urljoin

    request = urlopen(url)
    soup = BeautifulSoup(request.read(), 'lxml')
    base_url: str = "https://www.imperial.ac.uk"
    return [urljoin(base_url, url.get('href')) for url in soup.select('.col.event.lg-3.md-6.xs-12 a[href ]')]


async def scraping(url: str):

    import asyncio
    from typing import NoReturn, List, Tuple, Dict, Any, Union, Awaitable, Coroutine
    from os import path, getcwd
    from time import sleep
    import re, logging, asyncio, aiohttp
    from logger import creating_log
    from bs4 import element


    class ScrapeEvent:
        """ 
        The codebase design uses a single Class( dataclass) with it Methods as function scraping singular data (some more though).
        Returns the "self" to a it caller which is handled by a context manager.
        """
        soup: BeautifulSoup

        async def find_first_txt(self, css_selector: str) -> str:
            return await res[-1].get_text() if (res := self.soup.select(css_selector, limit=1)) else ""


        async def find_first(self, css_selector: str) -> BeautifulSoup:
            return await res[-1] if (res := self.soup.select(css_selector, limit=1)) else ""


        async def find_all(self, css_selector: str) -> List[element.Tag]:
            return await self.soup.select(css_selector)


        async def scrape_event_name(self) -> Union[str, str]:
            try:
                sc_event_name = self.find_first_txt('.page-heading h1')
            except Exception as e:
                ...
            else:
                return sc_event_name
            
            return ''

        
        async def scrape_event_type(self) -> Union[str, str]:
            try:
                sc_event_type = self.find_first_txt('.feature.topic span')
            except Exception as e:
                ...
            else:
                return sc_event_type
            
            return ''


        async def scrape_event_date(self) -> Union[str, str]:
            try:
                sc_event_date = self.find_first_txt('.event-details__date').replace('Date', '').strip()
            except Exception as e:
                ...
            else:
                return  sc_event_date
            
            return  ''


        async def scrape_event_time(self) -> Union[str, str]:
            try:
                sc_event_time = self.find_first_txt('.event-details__time')
            except Exception as e:
                ...
            else:
                return  sc_event_time
            
            return  ''

        
        async def scrape_event_venue(self) -> Union[str, str]:
            try:
                sc_event_venue = self.find_first_txt('.event-details__address')
            except Exception as e:
                ...
            else:
                return  sc_event_venue.replace('Location: ', '')
            
            return  ''


        async def scrape_event_cost(self) -> Union[str, str]:
            try:
                sc_event_cost = self.find_first_txt('.event-details__label +span')
            except Exception as e:
                ...
            else:
                return  sc_event_cost
            
            return  ''


        async def scrape_event_contact(self) -> Union[str, str]:
            try:
                sc_event_contact = self.find_first_txt('.event-details__label + a')
            except Exception as e:
                ...
            else:
                return  sc_event_contact
            
            return  ''

        async def scrape_event_contactMail(self) -> Union[str, str]:
            try:
                sc_event_contactMail = self.find_first('.event-details__label + a').get('href')
            except Exception as e:
                ...
            else:
                return  sc_event_contactMail.replace('mailto:', '')
            
            return  ''

        async def scrape_event_info(self) -> Union[str, str]:
            try:
                sc_event_info = self.find_first_txt('.event-details__label + a')
            except Exception as e:
                ...
            else:
                return  sc_event_info
            
            return  ''

        

        async def __call__(self, *args: Any, **kwds: Any) -> Any:
            ...


__all__ = ["get_all_urls", "scraping"]
            


