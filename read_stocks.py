import pandas as pd
import glob
from os.path import basename, splitext

filenames = glob.glob('dataset/nse/stocks/*.csv')
dfs_nse = {splitext(basename(fp))[0]: pd.read_csv(fp) for fp in filenames}

# Date,Symbol,Series,Prev Close,Open,High,Low,Last,Close,VWAP,Volume,Turnover,
# Trades,Deliverable Volume,%Deliverble
for i in dfs_nse:
    dfs_nse[i] = dfs_nse[i].rename(
        columns={
            'Deliverable Volume': 'Deliverable',
            "%Deliverble": "Percent Deliverable"})

filenames = glob.glob('dataset/bse/stocks/*.csv')
dfs_bse = {splitext(basename(fp))[0]: pd.read_csv(fp) for fp in filenames}

# Date,Open Price,High Price,Low Price,Close Price,WAP,No.of Shares,
# No. of Trades,Total Turnover (Rs.),Deliverable Quantity,
# % Deli. Qty to Traded Qty,Spread High-Low,Spread Close-Open
for i in dfs_bse:
    dfs_bse[i] = dfs_bse[i].rename(
        columns={
            'Open Price': 'BSE Open',
            'High Price': 'BSE High',
            'Low Price': 'BSE Low',
            'Close Price': 'BSE Close',
            'WAP': 'BSE WAP',
            'No.of Shares': 'BSE Volume',
            'No. of Trades': 'BSE Trades',
            'Total Turnover (Rs.)': 'BSE Turnover',
            'Deliverable Quantity': 'BSE Deliverable',
            '% Deli. Qty to Traded Qty': 'BSE Percent Deliverable to Traded'})
dfs_merged = {}

for i in dfs_nse:
    dfs_merged[i] = pd.merge(dfs_nse[i], dfs_bse[i], on='Date', how='outer')

for i in dfs_merged:
    dfs_merged[i].to_csv('dataset/active/'+i+'.csv', index=False)

# for i in dfs:
#     for j in dfs[i].columns:
#         dfs[i][j] = dfs[i][j].interpolate(
#             method='linear',
#             limit_direction='backward')
#     print(i + ": " + str(dfs[i].shape[0] - dfs[i].dropna().shape[0]))
#     print(dfs[i])
