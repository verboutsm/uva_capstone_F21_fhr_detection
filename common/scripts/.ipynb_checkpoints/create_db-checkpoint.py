import wdfb
from IPython.display import display
import matplotlib.pyplot as plt
import numpy as np
import os
import pandas as pd
from tqdm import tqdm


def get_all_records(data_loc):
    rec_list = []
    for file in os.listdir(data_loc):
        rec = file[:file.find('.')]
        try:
            rec = int(rec)
            rec_list.append(rec)
        except:
            pass
    rec_list = [str(i) for i in rec_list]
    return rec_list

def create_signals_database(rec, data_loc):
    sample = wfdb.rdsamp(data_loc + str(rec))
    df = pd.DataFrame(sample[0], columns=['FHR','UC'])
    df.index.name = 'seconds'
    df.to_csv('database/signals/%s.csv' % rec)
    
    
def create_ann_dataframe(rec, data_loc):
    sample = wfdb.rdsamp(data_loc + str(rec))
    ann = sample[1]['comments'][1:]
    ann_dic = {}
    for a in ann:
        if '--' in a:
            ann.remove(a)

    for a in ann:
        key = a[:a.find('  ')]
        if a.find('  ') == -1:
            key = a[:a.find(' ')]
        inv = a[::-1]
        value = inv[:inv.find(' ')][::-1]
        value = float(value)
        ann_dic[key] = [value]
        
    df1 = pd.DataFrame.from_dict(ann_dic).T
    df1 = df1.rename(columns={0:rec})
    return df1

def append_ann_dataframes(df,df1):
    rec = df1.columns[0]
    df[rec] = df1[rec]
    return df

def db_to_csv(data_loc)
    df = pd.DataFrame()
    for rec in tqdm(get_all_records(data_loc)):
        create_signals_database(rec, data_loc)
        df = append_ann_dataframes(df,create_ann_dataframe(rec))
    df.to_csv('database/ann_db.csv')