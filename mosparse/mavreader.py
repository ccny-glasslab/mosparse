import gzip
import zlib
from pathlib import Path

class MavReader:
    ''' Opens AVNMAV file and returns stream of data
    '''
    def __init__(self, filepath):
        self.filepath = Path(filepath)
        self.stream = "hello hello"
        if not self.filepath.exists():
            raise FileNotFoundError(f"{self.filepath}")
        
    def __enter__(self):
        if self.filepath.suffix == '.gz':
            #self._get_stations_gz()
        elif self.filepath.suffix == '.Z':
            #self._get_stations_z()
        else:
            #self._get_stations_other()
        return self.stream
    
    def __exit__(self, exc_type, exc_value, exc_traceback):
        pass
            
    
    def _get_stations_other(self):
        '''
        Opens and reads files that are not .Z and .gz formats.

        Parameters
        -----------
        path : string 
            Directions to the file you are going to use.

        Returns
        --------
        station : list of strings
            The data collected by the model.
        '''

        with open(path, 'rb') as f:
            self.f = f
    
    def _get_stations_z(self):
        '''
        Opens and reads files that are of the format .Z.

        Parameters
        -----------
        path : string 
            Directions to the file you are going to use.

        Returns
        --------
        station : list of strings
            The data collected by the model.
        '''
        from unlzw import unlzw
        with open(path, 'rb') as fh:
            compressed_data = fh.read()
            uncompressed_data = unlzw(compressed_data)
            uncompressed_data = uncompressed_data.split(b'\n')
            for i in range(len(uncompressed_data)):
                uncompressed_data[i] = uncompressed_data[i] + b'\n'
           # print(uncompressed_data[0:20])
            #uncompressed_data =           uncompressed_data.decode(errors='ignore').split('\n')
        #for i in range(len(uncompressed_data)):
        #    uncompressed_data[i] = (uncompressed_data[i] + '\n').encode()
        return get_main_stations(uncompressed_data)
        
    def self._get_stations_gz(self):
        '''
        Opens and reads files that are of the format .gz

        Parameters
        ------------
        path : string 
            Directions to the file you are going to use.

        Returns
        --------
        station : list of strings
            The data collected by the model.
        '''
        with gzip.open(path,'r') as f:
            return get_main_stations(f)
