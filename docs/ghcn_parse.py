import gzip
from pathlib import Path
import pandas as pd
import dask.dataframe as dd
import glob
import geopandas as gpd
import os
from pathlib import Path

df_stn = pd.read_csv('ghcnd_stations.csv')

def ghcn_parse(filepath):
    recorded_data = ['TMAX', 'TMIN', 'PRCP', 'SNOW', 'SNWD']
    accepted_sources = ['0', '7', 'A', 'B', 'F', 'H', 'K', 'M', 'N', 'R', 'T', 'U', 'W', 'X']

    f = gzip.open(filepath, 'r')
    stations={}
    #stations['Values'] = {'TMAX':'TMAX', 'TMIN':'TMIN', 'PRCP':'PRCP', 'SNOW':'SNOW', 'SNWD':'SNWD'}
    day = -999
    for line in f:
        l = line.decode().strip().split(',')
        if day!=l[1]:
            if day!=-999:
                df = pd.DataFrame(data=stations)
                df = df.transpose()
                df = pd.merge(df, df_stn, how='inner', on='0STN')
                df.to_csv(r'ghcn_days/'+day+'.csv', index=None)

            day = l[1]
        if l[2] in recorded_data and l[6] in accepted_sources:
            new_key =  l[0]
            if new_key not in stations.keys():
                stations[new_key] = {'0STN':l[0]}
            stations[new_key][l[2]]=float(l[3])
    df = pd.DataFrame(data=stations)
    df = df.transpose()
    df = pd.merge(df, df_stn, how='inner', on='0STN')
    df.to_csv(r'ghcn_days/'+day+'.csv', index=None)
    
def pandas_flip_csv(group, dfg):
    filepath = Path('ghcn_days', str(group)+'.csv.gz')
    if not filepath.exists():
        dfg = dfg.pivot(index='Station', columns='Observation Type', values='Observation')
        dfg = dfg[['TMAX', 'TMIN', 'PRCP', 'SNOW', 'SNWD']]
        dfg = dfg.merge(df_stn, left_on="Station", right_on="0STN", how="inner")
        dfg.to_csv(Path('ghcn_days', f'{group}.csv.gz'), index=None, compression='gzip')
        del(dfg)