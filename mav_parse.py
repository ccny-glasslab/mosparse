import dateutil
import pandas as pd
import numpy as np
# make a station object 

integer = ['TMP', 'DPT', 'WDR', 'WSP', 'CIG', 'VIS', 'N/X', 'P06', 'P12', 'POS', 'POZ','SNW']
categorical = ['CLD','OBV', 'TYP', 'Q06', 'Q12', 'T06', 'T12']
incremental = ['N/X', 'P06', 'P12', 'Q06', 'Q12','T06', 'T12','SNW']
incremental2 = ['T06' , 'T12']

def get_header(header_row):
    header = {}
    header['station'], c1, c2, c3, date, time, tz =  header_row.split()
    header['model'] = f'{c1} {c2} {c3}' 
    header['runtime'] = dateutil.parser.parse(f'{date} {time} {tz}')
    return header

def get_fntime(date_row, hour_row, header):
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
        month, day = dates[dt].split()
        # half the values are strings, so create full string to parse
        # otherwise would have to cast to string or int
        fntime = f'{year} {month} {day} {hour}'
        finish_times.append(dateutil.parser.parse(fntime))
    return finish_times

def parse_incremental(row):
    var = row[:6].strip()
    row = row.rstrip('\n')
    vals = []
    for i in range(6, len(row),3):
        val = row[i:i+3].strip()
        if val is not '':
            vals.append(row[i:i+3].strip())
        else:
            vals.append(None)
    return var, vals

def parse_incremental2(row):
    var = row[:6].strip()
    row = row.rstrip('\n')
    vals = []
    vals.append(None)
    for i in range(9, len(row),6):
        vals.append(None)
        val = row[i:i+6].strip()
        if val is not '':
            vals.append(row[i:i+6].strip())
        else:
            vals.append(None)
    return var, vals

def get_rows(header, station):
    df = pd.DataFrame(header)
    for row in station[3:]:
        #cranky parsing issues
        if row.startswith(tuple(incremental), 1):
            if row.startswith(tuple(incremental2),1):
                var, vals = parse_incremental2(row)
            else:
                var, vals = parse_incremental(row)
        else:
            var, *vals = row.split()
        # data type
        if var in categorical:
            df[var] = np.array(vals, dtype='object')
        elif var in integer: # cast to int
            df[var] = np.array(vals, dtype='float64')
        else:
            raise KeyError(f"{var} parsing not supported")
    return df

def parse_station(station):
    header = get_header(station[0])
    header['ftime']= get_fntime(station[1], station[2], header)
    df = get_rows(header, station)
    return df