from pathlib import Path

from tqdm.auto import tqdm

import mosparse.mavreader as mpr
import mosparse.mavtodb as mdb 

mos_files = list(Path("../../avnmav/").iterdir())

with open("completed_files.txt", 'a') as f:
    for path in tqdm(mos_files):
        with mpr.MavReader(path, stations=True) as station_generator:
            with tqdm(desc=path.name, position=1) as pbar:
                for station in station_generator:
                    if len(station)>0:
                        mdb.station_to_db(station)
                    pbar.update(1)
        print(path.name, file=f)
