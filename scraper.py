from bs4 import BeautifulSoup
from typing import List
from . import data_cleaning

large_num: int = 1000
start_url: str = f"https://www.imperial.ac.uk/whats-on/?audience=&match=any&quantity={large_num}&show=future&start=0&tags=institutional-event"

def get_all_urls(url: str = start_url, BeautifulSoup: BeautifulSoup = BeautifulSoup) -> List[str]:
    from urllib.request import urlopen
    from urllib.parse import urljoin

    request = urlopen(url)
    soup = BeautifulSoup(request.read(), 'lxml')
    base_url: str = "https://www.imperial.ac.uk"
    return [urljoin(base_url, url.get('href')) for url in soup.select('.col.event.lg-3.md-6.xs-12 a[href ]')]


async def scraping(url: str, instance_name: str):

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
            return await res[0].get_text() if (res := self.soup.select(css_selector, limit=1)) else ""


        async def find_first(self, css_selector: str) -> BeautifulSoup:
            return await res[0] if (res := self.soup.select(css_selector, limit=1)) else ""


        async def find_all(self, css_selector: str) -> List[element.Tag]:
            return await self.soup.select(css_selector)


        async def scrape_event_name(self) -> Union[str, str]:
            try:
                sc_event_name = self.find_first_txt('.page-heading h1')
            except Exception as e: ...
            else:
                return sc_event_name


        async def scrape_event_type(self) -> Union[str, str]:
            try:
                sc_event_type = self.find_first_txt('.feature.topic span')
            except Exception as e: ...
            else:
                return sc_event_type


        async def scrape_event_date_time(self) -> Union[Dict[str, str], str]:
            try:
                sc_event_start = self.find_first('.event-details__block [itemprop="startDate"]')
                sc_event_end = self.find_first('.event-details__block [itemprop="endDate"]')
            except Exception as e: ...
            else:
                return data_cleaning.date_and_time(sc_event_start, sc_event_end)
            
        
        async def scrape_event_venue(self) -> Union[Dict[str, str], str]:
            try:
                sc_event_location = self.find_first_txt('.event-details__address').replace('\n', '').strip()
                sc_event_campus = self.find_first_txt('.event-details__venue').replace('\n', '').strip()
            except Exception as e: ...
            else:
                return  {"location": sc_event_location, "campus": sc_event_campus}


        async def scrape_event_cost(self) -> Union[Dict[str, str], str]:
            try:
                sc_event_cost = self.find_first_txt('.event-details__label + span')
            except Exception as e: ...
            else:
                if sc_event_cost.lower() == 'free': return {"currency": "", "price": ""}
                else: return {"currency": sc_event_cost[0] if sc_event_cost != None else "",
                            "price": sc_event_cost[1:] if sc_event_cost != None else ""}
            
            
        async def scrape_event_contact(self) -> List[Dict[str, str]]:
            try:
                sc_event_contact = self.find_all('.event-details__label + a')
            except Exception as e: ...
            else:
                container: List[Dict[str, str]] = []
                for info in sc_event_contact:
                    container.append({"name": info.get_text().replace('\n', '').strip(), "link": info.get('href')}) if info  else ...
                return container

            
        async def scrape_event_info(self) -> Union[str, str]:
            try:
                sc_event_info = self.find_first_txt('.content-hero__body p')
            except Exception as e: ...
            else:
                return  sc_event_info


        async def __call__(self, *args: Any, **kwds: Any) -> Any:
            funcs = (getattr(self, name) for name in dir(self) if name.startswith('scrape'))
            for i in funcs:
                i()

    instance_name = ScrapeEvent(url)
    instance_name()

__all__ = ["get_all_urls", "scraping"]
            


