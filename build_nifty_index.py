import pandas as pd
import glob
from os.path import basename, splitext

filenames = glob.glob('dataset/nse/index/yearly/*.csv')
li = []

for i in filenames:
    df = pd.read_csv(i, index_col=None, header=0)
    li.append(df)

frame = pd.concat(li, axis=0, ignore_index=True)

frame.to_csv('dataset/nse/index/NIFTY50.csv', index=False)
