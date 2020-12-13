import pandas as pd
import glob
from os.path import basename, splitext

filenames = glob.glob('dataset/active/*.csv')
dfs_merged = {splitext(basename(fp))[0]: pd.read_csv(fp) for fp in filenames}

for i in dfs_merged:
    print(
        i + ": " +
        str(dfs_merged[i].shape[0] - dfs_merged[i].dropna().shape[0]))
