import pandas as pd
import glob
from os.path import basename, splitext

# index_frame = pd.read_csv('dataset/nse/index/NIFTY50.csv')
# index_frame['Date'] = pd.to_datetime(index_frame['Date'], format='%d-%b-%Y')
# index_frame.to_csv('dataset/nse/index/NIFTY50_datefix.csv', index=False)

filenames = glob.glob('dataset/bse/stocks/*.csv')
dfs_bse = {splitext(basename(fp))[0]: pd.read_csv(fp) for fp in filenames}

for i in dfs_bse:
    dfs_bse[i]['Date'] = pd.to_datetime(dfs_bse[i]['Date'], format='%d-%B-%Y')
    dfs_bse[i].to_csv('dataset/bse/stocks/'+i+'.csv', index=False)
