import pandas as pd
import numpy as np
import gzip


class SOMToolBox_Parse:
    
    def __init__(self, filename):
        self.filename = filename
    
    def read_weight_file(self,):
        df = {}
        if self.filename[-3:len(self.filename)] == '.gz':
            with gzip.open(self.filename, 'rb') as file:
                df = self._read_vector_file_to_df(df, file)
               #df['arr'] = np.rot90(df['arr'].reshape(df['ydim'],df['xdim'],df['vec_dim'])).reshape(-1,df['vec_dim']) #rotate matrix because of SOMToolbox format

        else:
            with open(self.filename, 'rb') as file:
                df = self._read_vector_file_to_df(df, file)

        file.close()

        return df
    
    def _read_vector_file_to_df(self, df, file):
        for byte in file:
            line = byte.decode('UTF-8')
            if line.startswith('$'):
                df = self._parse_vector_file_metadata(line, df)
            else:
                c = df['vec_dim'] if 'vec_dim' in df else 2 
                if 'arr' not in df: df['arr'] = np.empty((0,c), dtype=float)
                df = self._parse_weight_file_data(line, df)
        return df


    def _parse_weight_file_data(self, line, df):
        splitted=line.split(' ')
        try:
            c = df['vec_dim'] if 'vec_dim' in df else 2
            df['arr'] = np.append(df['arr'], [np.array(splitted[0:c]).astype(float)], axis=0)
        except: raise ValueError('The input-vector file does not match its unit-dimension.') 
        return  df

    def _parse_vector_file_metadata(self, line, df):
        splitted = line.strip().split(' ')
        if splitted[0]   == '$XDIM':        df['xdim']          = int(splitted[1])
        elif splitted[0] == '$YDIM':        df['ydim']          = int(splitted[1])
        elif splitted[0] == '$VEC_DIM':     df['vec_dim']       = int(splitted[1])
        elif splitted[0] == '$CLASS_NAMES': df['classes_names'] = splitted[1:] 
        return df 
        