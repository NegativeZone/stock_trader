import pandas as pd

filenames = [
    "HDFCBANK"
]

dfs = {}
for i in filenames:
    dfs[i] = pd.read_csv("dataset/ML/"+i+".csv")
    dfs[i]['Change'] = dfs[i]["Close"] - dfs[i]["Open"]
    dfs[i]['Date'] = pd.to_datetime(
        dfs[i]['Date'], format='%Y-%m-%d', errors='coerce')
    dfs[i]['Movement'] = dfs[i]['Change'].apply(
        lambda x: 1 if x > 0 else 0)
    dfs[i] = dfs[i].sort_values(by="Date")
    dfs[i] = dfs[i].reset_index(drop=True)
    dfs[i] = dfs[i].drop(columns=["Date", "Symbol"])
    print(dfs[i])
