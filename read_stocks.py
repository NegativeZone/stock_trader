import pandas as pd
import glob
from os.path import basename, splitext

filenames = glob.glob('dataset/nse/stocks/*.csv')
dfs = {splitext(basename(fp))[0]: pd.read_csv(fp) for fp in filenames}

print(dfs['BAJAJ-AUTO'].columns)
