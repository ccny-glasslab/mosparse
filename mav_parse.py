import os
import re
import dateutil
import datetime
import gzip
import zlib
from pathlib import Path
import traceback

import pandas as pd
import numpy as np

empty= re.compile(b'\s+\n')
newline = re.compile(b'1\n')

integer = ['TMP', 'DPT', 'WDR', 'WSP', 'CIG', 'VIS', 'N/X', 'P06', 'P12', 'POS', 'POZ','SNW']
categorical = ['CLD','OBV', 'TYP', 'Q06', 'Q12', 'T06', 'T12']
incremental = ['N/X', 'P06', 'P12', 'Q06', 'Q12','T06', 'T12','SNW']
incremental2 = ['T06' , 'T12']

def get_header(header_row):
    """ Creates a dictionary containing the station, model, and run time based on the first row of the MOS data. The row should only come from MOS data.

    Parameters:
    header_row: string

    Returns:
    header: dictionary
    """
    header = {}
    header['station'], c1, c2, c3, date, time, tz =  header_row.split()
    header['short_model'] = c1
    header['model'] = f'{c1} {c2} {c3}' 
    header['runtime'] = dateutil.parser.parse(f'{date} {time} {tz}')
    return header

def get_fntime(date_row, hour_row, header):
    """ Creates a list of dateutil dates based on a header and the date and hour rows of the MOS data.
        
    Parameters:
    date_row: string
    hour_row: string
    header: dictionary
    
    Returns:
    finish_times: list
    """
    #(DT, Hr tuples), which is the finish time column
    #http://www.meteor.wisc.edu/~hopkins/aos100/mos-doc.htm
    #https://mesonet.agron.iastate.edu/mos/fe.phtml
    dates = [m.strip() for m in date_row.split("/")[1:]]
    hours = [dt.strip() for dt in hour_row.split()][1:]
    
    year = header['runtime'].year
    
    finish_times = []
    dt = -1
    for hour in hours:
        if hour == '00':
            dt+=1
        #try:   
        month, day = dates[dt].split()
       # except:
       #     if dt > 0:
       #         prevmonth, prevday = dates[dt-1].split()
       #         currdate = datetime.datetime(int(year), int(prevmonth), int(prevday)) + datetime.timedelta(days=1)
       #         month, day = currdate.month, currdate.day
       #     else:
       #         prevmonth, prevday = dates[dt+1].split()
       #         currdate = datetime.datetime(int(year), int(prevmonth), int(prevday)) - datetime.timedelta(days=1)
       #         month, day = currdate.month, currdate.day
            
        # half the values are strings, so create full string to parse
        # otherwise would have to cast to string or int
        fntime = f'{year} {month} {day} {hour}'
        finish_times.append(dateutil.parser.parse(fntime))
    return finish_times

def parse_row(row):
    """Takes a row of MOS data and returns the variable and a list of values.
   
    Parameters:
    row: string
    Returns:
    var: string
    vals: list
    """
    var = row[:5].strip()
    row = row.rstrip('\n')
    vals = []
    for i in range(5, len(row)-1,3):
        val = row[i:i+3].strip()
        if ('/' in val):
            vals[-1] = None
            vals.append(row[i-3:i+3].strip())
        elif val is not '':
            vals.append(row[i:i+3].strip())
        else:
            vals.append(None)
    return var, vals

def get_rows(header, station):
    """ Produces a numpy array of station data based on a previously produced header and a list of MOS station data.

    Parameters:
    header: dictionary
    station: list of strings

    Returns:
        df: numpy array
    """
    df = pd.DataFrame(header)
    for row in station[3:]:
        #cranky parsing issues
        var, vals = parse_row(row)
        # data type
        
        if var in categorical:
            df[var] = np.array(vals, dtype='object')
        elif var in integer: # cast to int
            df[var] = np.array(vals, dtype='float64')
        else:
            raise KeyError(f"{var} parsing not supported")
        
    return df

def parse_station(station):
    """Creates a numpy array of station data from a list of MOS station data.
Incorporates get_header, get_fntime, and get_rows.

    Parameters:
    station: list of strings 

    Returns:
    df: numpy array
    """
    if not station:
        return pd.DataFrame()
    header = get_header(station[0])
    header['ftime']= get_fntime(station[1], station[2], header)
    df = get_rows(header, station)
    return df

def write_station(station, saveout="modelruns", logs="log"):
    if not station:
        return

    if not Path(saveout).exists():
        os.mkdir(saveout)
    
    if not Path(logs).exists():
        os.mkdir(logs)

    try:
        header = get_header(station[0])
        runtime = str(header['runtime'])
        name = f"{header['short_model']}_{header['station']}_{header['runtime'].strftime('%Y_%m_%d_%H')}"
        filename = f"{name}.csv"
        filepath = Path(saveout,filename)    
        if not filepath.exists():
            header['ftime']= get_fntime(station[1], station[2], header)
            df = get_rows(header, station)
            df.to_csv(filepath, index=False)
    except Exception as e:
        with open(Path(logs,f'{filename}.log'), 'w') as f:
            print(station, file=f)
            traceback.print_exc(file=f)
            
    return

def _get_stations_other(path):
    with open(path, 'rb') as f:
        return get_main_stations(f)
def _get_stations_z(path):
    from unlzw import unlzw
    
    with open(path, 'rb') as fh:
        compressed_data = fh.read()
        #print('A')
        uncompressed_data = unlzw(compressed_data)
        uncompressed_data = uncompressed_data.decode(errors='ignore').split('\n')
        for i in range(len(uncompressed_data)):
            uncompressed_data[i] = uncompressed_data[i] + '\n'
            uncompressed_data[i] = uncompressed_data[i].encode()
        #print(uncompressed_data[0:20])
        #print('B')
        return get_main_stations(uncompressed_data)
        print('Z')
def _get_stations_gz(path):
    with gzip.open(path,'r') as f:
        return get_main_stations(f)

def get_stations(path):
    name, ext = os.path.splitext(path)
    #print(ext, path)
    if ext == '.gz':
        return _get_stations_gz(path)
    elif ext == '.Z':
        return _get_stations_z(path)
    else:
        return _get_stations_other(path)
    try:
        get_stations(path)
    except Exceptions as e:
        print(e, path)
def get_main_stations(f):
    station = []
    stations = []
    #print('C')
    for i, line in enumerate(f):
            if empty.match(line):
                stations.append(station)
                station = []
                #print('ABC')
            elif newline.match(line):
                #print('DEF')
                pass
            else:
                station.append(line.decode())
                #print('GHI')
    #print('D')
    return stations
