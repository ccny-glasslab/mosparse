import os
import re
import dateutil
import datetime
from pathlib import Path
import traceback

import pandas as pd
import numpy as np

import logging

LOG_FILENAME = Path('moslog.out')
(LOG_FILENAME.parent).mkdir(parents=True, exist_ok=True)
logger = logging.getLogger("database")
logger.setLevel(logging.INFO)
handler = logging.FileHandler(filename=LOG_FILENAME)
logger.addHandler(handler)



integer = ['N/X', 'X/N', 'TMP', 'DPT', 'WDR', 'WSP', 'CIG', 'VIS', 'P06', 'P12', 'POS', 'POZ','SNW']
categorical = ['CLD','OBV', 'TYP', 'Q06', 'Q12', 'T06', 'T12']
all_cols = integer + categorical
# pop N/X
all_df = pd.DataFrame(columns=all_cols[1:]) 
#incremental = ['N/X', 'X/N', 'P06', 'P12', 'Q06', 'Q12','T06', 'T12','SNW']
#incremental2 = ['T06' , 'T12']

def get_header(header_row):
    """ 
    Creates a dictionary containing the station, model, and run time based on the first row of the MOS data. 
    The row should only come from MOS data.

    Parameters
    -----------
    header_row : string
        Row with name, model, and runtime of a station.

    Returns
    --------
    header : dictionary
        Values of the name, model, and runtime of a station.
    """
    header = {}
    header['station'], c1, c2, c3, date, time, tz =  header_row.split()
    header['short_model'] = c1
    header['model'] = f'{c1} {c2} {c3}' 
    header['runtime'] = dateutil.parser.parse(f'{date} {time} {tz}')
    return header

def get_fntime(date_row, hour_row, header):
    """ 
    Creates a list of dateutil dates based on a header and the date and hour rows of the MOS data.
        
    Parameters
    -----------
    date_row : string
        The dates the model is predicting 
    hour_row : string
        The hours the model is prediction
    header : dictionary
        Values of the name, model, and runtime of a station.

    Returns
    --------
    finish_times : list
        List of the time in hour the model stopped running.
    forecast_times : list
        List of the amount of hours the model is predicting in advance.
        
    """
    #(DT, Hr tuples), which is the finish time column
    #http://www.meteor.wisc.edu/~hopkins/aos100/mos-doc.htm
    #https://mesonet.agron.iastate.edu/mos/fe.phtml
    dates = [m.strip() for m in date_row.split("/")[1:]]
    hours = [dt.strip() for dt in hour_row.split()][1:]
    
    year = header['runtime'].year
    
    finish_times = []
    dt = 0
    first_stopped = 0
    for hour in hours:
        if first_stopped == 0:
            first_stopped = 1
        elif hour == '00':
            dt+=1
        try:
            currdate = dateutil.parser.parse(dates[dt])
            month, day = currdate.month, currdate.day
            if month == 1 and day == 1 and hour == '00':
                year += 1
        except:
            #if dt > 0:
            currdate = dateutil.parser.parse(str(year) + ' ' + dates[dt-1]) + datetime.timedelta(days=1)
            year, month, day = currdate.year, currdate.month, currdate.day
            #else:
            #    prevmonth, prevday = dates[dt+1].split()
             #   currdate = datetime.datetime(int(year), int(prevmonth), int(prevday)) - datetime.timedelta(days=1)
              #  month, day = currdate.month, currdate.day
            
        # half the values are strings, so create full string to parse
        # otherwise would have to cast to string or int
        fntime = f'{year} {month} {day} {hour}'
        finish_times.append(dateutil.parser.parse(fntime))
        #forecast_times.append(int((((finish_times[-1])-(header['runtime'].replace(tzinfo=None))).total_seconds())/3600))
    return finish_times #also finish_times

def parse_row(row):
    """
    Takes a row of MOS data and returns the variable and a list of values.
   
    Parameters
    -----------
    row : string
        The rows where the data collected is stored.
    
    Returns
    --------
    var : string
        Value spaces that are part of the rows
    vals : list
        Value that are part of the rows
    """
    var = row[:5].strip()
    row = row.rstrip('\n')
    vals = []
    for i in range(5, len(row)-1,3):
        val = row[i:i+3].strip()
        if ('/' in val):
            vals[-1] = None
            vals.append(row[i-3:i+3].strip())
        elif val != '':
            vals.append(row[i:i+3].strip())
        else:
            vals.append(None)
    return var, vals

def get_rows(header, station):
    """ 
    Produces a numpy array of station data based on a previously produced header and a list of MOS station data.

    Parameters
    -----------
    header : dictionary
        Values of the name, model, and runtime of a station.
    station : list of strings
        All the data colleceted by the model.

    Returns
    --------
    df : numpy array
        Header and station pt together.
    """
    df = pd.DataFrame(header, columns=list(header.keys()) + all_cols)
    for row in station[3:]:
        #cranky parsing issues
        var, vals = parse_row(row)
        # data type
        
        if var in categorical:
            #try:
            df[var] = np.array(vals, dtype='object')

        elif var in integer: # cast to int
            if (var == 'N/X'):
                df['X/N'] = np.array(vals, dtype='float64')
            else:
                #try:
                df[var] = np.array(vals, dtype='object')

        else:
            raise KeyError(f"{var} parsing not supported")
        
    return df

def parse_station(station):
    """
    Creates a numpy array of station data from a list of MOS station data.
Incorporates get_header, get_fntime, and get_rows.

    Parameters
    -----------
    station : list of strings 
        The data collected by the model.

    Returns
    --------
    df : numpy array
        Header and station pt together.
    """
    if not station:
        return pd.DataFrame()
    header = get_header(station[0])
    header['ftime'] = get_fntime(station[1], station[2], header) 
    df = get_rows(header, station)
    return df

def write_station(station, filename = None, stations = None, columns= None, saveout="mos/modelrun",logs="mos/log"):
    '''
    Seperates the stations with errors and the stations without errors into folders log and modelruns, respectively.
    
    Parameters
    -----------
    station : list of strings
        The data collected by the model.
    
    saveout : string
        Folder where the stations without errors are stored.
    
    log : string
        Folder where the stations with errors are stored.
    
    Returns
    --------
    station : list of strings
        The data collected by the model.
    '''
    if not station:
        return
    
    # hack to check the station code, skip parsing if not in list
    if (stations is not None) and (stations[0][:5].strip() not in stations):
        return
        
    Path(saveout).mkdir(parents=True, exist_ok=True)
    Path(logs).mkdir(parents=True, exist_ok=True)
    
    try:
        df = parse_station(station)
        station = df['station'].unique()[0]
        short_model = df['short_model'].unique()[0]   
        runtime = df['runtime'].unique()[0]
    except Exception as e:
        header = get_header(station[0])
        short_model = header['short_model']
        runtime = header['runtime']
        logger.exception("{station}: {runtime:%Y/%m/%d:%H}".format(**header))
    else:
        filename = f"{short_model}_{runtime:%Y_%m_%d_%H}.csv" if filename is None else filename
        filepath = Path(saveout, filename) 
        mode = 'a' if filepath.exists() else 'w'
        columns = df.columns if columns is None else columns
        df[columns].to_csv(filepath, index=False, mode=mode, header=False)
        logger.info(f"{station}: {runtime:%Y/%m/%d:%H}")
    return filepath