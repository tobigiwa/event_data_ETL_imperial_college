from dataclasses import dataclass
from typing import NoReturn, List, Tuple, Dict
from os import path, getcwd
from time import sleep
from logger import creating_log
import re, logging

logger: logging = creating_log()


@dataclass
class ScrapeEvent:
    """ 
    The codebase design uses a single Class( dataclass) with it Methods as function scraping singular data (some more though).
    Returns the "self" to a it caller which is handled by a context manager.
    """


