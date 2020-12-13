import pandas as pd
import glob
from os.path import basename, splitext

filenames = glob.glob('dataset/nse/stocks/*.csv')
dfs_nse = {splitext(basename(fp))[0]: pd.read_csv(fp) for fp in filenames}

for i in dfs_nse:
    dfs_nse[i] = dfs_nse[i].rename(
        columns={"%Deliverble": "Percent Deliverable"})

filenames = glob.glob('dataset/bse/stocks/*.csv')
dfs_bse = {splitext(basename(fp))[0]: pd.read_csv(fp) for fp in filenames}

# print(dfs['BAJAJ-AUTO'].iloc[0])

# for i in dfs:
#     for j in dfs[i].columns:
#         dfs[i][j] = dfs[i][j].interpolate(
#             method='linear',
#             limit_direction='backward')
#     print(i + ": " + str(dfs[i].shape[0] - dfs[i].dropna().shape[0]))
#     print(dfs[i])
