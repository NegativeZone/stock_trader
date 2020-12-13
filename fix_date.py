import pandas as pd

index_frame = pd.read_csv('dataset/nse/index/NIFTY50.csv')
index_frame['Date'] = pd.to_datetime(index_frame['Date'], format='%d-%b-%Y')
index_frame.to_csv('dataset/nse/index/NIFTY50_datefix.csv', index=False)
