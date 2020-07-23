import io
import gzip
from pathlib import Path
import re
import zlib

from unlzw import unlzw

class MavReader:
    ''' Opens AVNMAV file and returns stream of data
    '''
    empty = re.compile(b'\s+\n')
    newline = re.compile(b'1\n')
    
    def __init__(self, filepath, stations=False):
        """Open a avnmav file and returns text or a generator of stations
        filepath: str or Path
            location of avnmav file
        stations: bool, default=False
            True: generator of list of stations
            False: stream of text
        """
        self.filepath = Path(filepath)
        if not self.filepath.exists():
            raise FileNotFoundError(f"{self.filepath}")
        self.stations = stations
        self.stream = None
        
    def __enter__(self):
        if self.filepath.suffix == '.gz':
            self.stream = gzip.open(self.filepath,'r')     
        elif self.filepath.suffix == '.Z':
            file_obj = open(self.filepath, 'rb')
            compressed_data = file_obj.read()
            self.stream = io.BytesIO(unlzw(compressed_data))
            file_obj.close()
        else:
            self.stream = open(self.filepath, 'rb')
        if self.stations:
            return self.get_stations()
        return self.stream
    
    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.stream.close()
            
    def get_stations(self):
        station = []
        for line in self.stream:
            if MavReader.empty.match(line):
                yield station
                station = []
            elif MavReader.newline.match(line):
                continue
            else:
                station.append(line.decode())
            
        

