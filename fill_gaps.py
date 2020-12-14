import pandas as pd
import glob
from os.path import basename, splitext

filenames = glob.glob('dataset/active/*.csv')
dfs_merged = {splitext(basename(fp))[0]: pd.read_csv(fp) for fp in filenames}

# for i in dfs_merged:
#     print(
#         i + ": " +
#         str(dfs_merged[i].shape[0] - dfs_merged[i].dropna().shape[0]))

dfs_2010 = {}
for i in dfs_merged:
    dfs_2010[i] = dfs_merged[i][(dfs_merged[i]['Date'] > '2011-05-31')]
    dfs_2010[i] = dfs_2010[i].interpolate(method='polynomial', order=3)
    dfs_2010[i] = dfs_2010[i].drop(columns='Series')
    dfs_2010[i]['Date'] = pd.to_datetime(
        dfs_2010[i]['Date'], format='%Y-%m-%d', errors='coerce')
    dfs_2010[i] = dfs_2010[i].sort_values(by=['Date'], ascending=False)

y = {}
X = {}
for i in dfs_2010:
    y[i] = []
    X[i] = []
    j = 0
    while j < dfs_2010[i].shape[0]:
        if (j+5 < dfs_2010[i].shape[0] and j+10 < dfs_2010[i].shape[0]):
            y[i].append(dfs_2010[i]['Close'].iloc[j:j+5].to_numpy())
            X[i].append(dfs_2010[i]['Close'].iloc[j+5:j+10].to_numpy())
        j += 5

print(len(X['ADANIPORTS']))
print(len(y['ADANIPORTS']))

# df_ML = pd.DataFrame()
#
# for i in dfs_2010:
#     df_ML = df_ML.append(dfs_2010[i], ignore_index=True)
#
# df_ML.to_csv('dataset/ML/data.csv', index=False)
