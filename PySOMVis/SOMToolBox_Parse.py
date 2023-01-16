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
                if df['type'] == 'vec' or df['type'] == 'som': c = df['vec_dim'] 
                else:   c = df['xdim']
                if 'arr' not in df: df['arr'] = np.empty((0, c), dtype=float)
                df = self._parse_weight_file_data(line, df, c)
        return df


    def _parse_weight_file_data(self, line, df, c):
        splitted=line.rstrip().split(' ')
        try:
            if df['type'] =='vec' or df['type'] =='class_information' or df['type'] =='som':
                res = np.array(splitted[0:c]).astype(float)
            else:
                res = np.array(splitted[0:c]).astype(str)
            df['arr'] = np.append(df['arr'], [res], axis=0)
        except: raise ValueError('The input-vector file does not match its unit-dimension.') 
        return  df

    def _parse_vector_file_metadata(self, line, df):
        splitted = line.strip().split(' ')
        if splitted[0]   == '$TYPE':        df['type']          = splitted[1]
        if splitted[0]   == '$XDIM':        df['xdim']          = int(splitted[1])
        elif splitted[0] == '$YDIM':        df['ydim']          = int(splitted[1])
        elif splitted[0] == '$VEC_DIM':     df['vec_dim']       = int(splitted[1])
        elif splitted[0] == '$CLASS_NAMES': df['classes_names'] = splitted[1:] 
        return df        