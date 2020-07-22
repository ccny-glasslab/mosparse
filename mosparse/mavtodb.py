import logging
from pathlib import Path

LOG_FILENAME = Path('mos/logmos2db.out')
(LOG_FILENAME.parent).mkdir(parents=True, exist_ok=True)
logger = logging.getLogger("database")
logger.setLevel(logging.INFO)
handler = logging.FileHandler(filename=LOG_FILENAME)
logger.addHandler(handler)

import sqlite3
# Create a SQL connection to our SQLite database
con = sqlite3.connect("mos.sqlite")

from mosparse.mavparse import get_header, parse_station
def station_to_db(station):
    '''
    parses station in dataframe and then adds all rows in 
    spreadsheet to database
    
    logs errors to LOG_FILENAME
    '''
    if not station:
        return
    try:
        df = parse_station(station)
        short_model = df['short_model'].unique()[0]   
    except Exception as e:
        header = get_header(station[0])
        logger.exception("{station}: {runtime:%Y/%m/%d:%H}".format(**header))
    else:
        df.to_sql(short_model, con=con, if_exists='append')
    return 