from typing import Union, Dict
from bs4 import element

def date_and_time(start_date: element.Tag, end_date: element.Tag) -> Union[Dict[str, str], str]:
    from datetime import datetime

    start = start_date.get('content').split("T") # content="2023-01-20T23:55:00+00:00"
    end = end_date.get('content').split("T") # content="2023-01-20T23:55:00+00:00"

    return  {"start_date": start[0], 
            "end_date": end[0],
            "start_time": datetime.strftime(start[1], '%H:%M:%S%z').strftime('%H:%M'),
            "end_time": datetime.strftime(end[1], '%H:%M:%S%z').strftime('%H:%M')
            }