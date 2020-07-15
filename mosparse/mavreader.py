import io
import gzip
from pathlib import Path
import zlib

from unlzw import unlzw

class MavReader:
    ''' Opens AVNMAV file and returns stream of data
    '''
    def __init__(self, filepath):
        self.filepath = Path(filepath)
        if not self.filepath.exists():
            raise FileNotFoundError(f"{self.filepath}")
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
        return self.stream
    
    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.stream.close()
            
    
    def get_stations_z(self):
        '''
        Opens and reads files that are of the format .Z..
        '''
   
       
        

