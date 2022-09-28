"""
Mark Febrizio

References:
- https://github.com/mementoweb/py-memento-client
- http://timetravel.mementoweb.org/guide/api/#memento-json
"""

# import dependencies
import datetime
from memento_client import MementoClient


def get_date_tuples(df, column = "date"):
    dates_list = list(map(lambda x: tuple(x.split(r"-")), df[column].values))
    #dates_list = list(map(lambda x: x[-1::] + x[0:-1], dates_list))
    dates_list = [tuple(map(lambda x: int(x), t)) for t in dates_list]
    return dates_list


def get_urls(df, column = "pi_url"):
    url_list = list(map(lambda x: x.split(r"#")[0], df[column].values))
    return url_list


def query_closest_memento(url: str, date_tuple: tuple):

    # set datetime
    yyyy, mm, dd = date_tuple
    dt = datetime.datetime(yyyy, mm, dd, 8, 15)
    
    # set url
    uri = url
    
    # get info from memento client
    mc = MementoClient()
    memento_uri = mc.get_memento_info(uri, dt)
    
    closest_uri = memento_uri.get("mementos").get("closest").get("uri")[0]
    
    return closest_uri

