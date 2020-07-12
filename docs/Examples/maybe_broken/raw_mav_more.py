import re
import gzip
import mav_parse as mp
import numpy as np
import dask.bag as db
from tqdm import tqdm, tqdm_notebook
from dask.diagnostics import ProgressBar

import glob
from pathlib import Path
#Path("/opt", "data", "avnmav", "avnmav").exists()
#files = glob.glob("/opt/data/avnmav/avnmav/mav*")

files = glob.glob('avnmav/mav*')
if not files:
    raise ValueError("files not found")

pb = db.from_sequence(files).map(mp.get_stations)
dfs = pb.flatten().map(mp.write_station)
with ProgressBar():
    dfs.compute()
