import os
import json
import pandas as pd
import numpy as np
import methods



file_size = os.path.getsize("[1]game_logs.csv")
data = pd.read_csv("[1]game_logs.csv")
print(f"Size without optimization: {data.memory_usage(deep=True).sum() // (1024 * 1024)} MB")
methods.getDataInfo(data, file_size, "memory_usage.json")

data_optimized = methods.optimizeData(data)
print(f"Size with optimization: {data_optimized.memory_usage(deep=True).sum() // (1024 * 1024)} MB")
methods.getDataInfo(data_optimized, file_size, "memory_usage_optimized.json")

columns = ["date", "number_of_game", "day_of_week", "park_id","v_manager_name", "length_minutes", "v_hits","h_hits", "h_walks", "h_errors"]
methods.optimizeData = methods.saveData(data_optimized, columns, "data_optimized_dtype.json")

flag_header = True
size = 0
with open("data_optimized_dtype.json", mode='r') as f:
        dtypes = json.load(f)
        
for elem in pd.read_csv("[1]game_logs.csv", usecols=lambda x: x in dtypes.keys(), dtype=dtypes,chunksize=500_000):
    size += elem.memory_usage(deep=True).sum()
    elem.dropna().to_csv("filtered_data.csv", mode="a", header=flag_header, index=False)
    flag_header = False

for key in dtypes.keys():
    if dtypes[key] == 'category':
        dtypes[key] = pd.CategoricalDtype
    else:
        dtypes[key] = np.dtype(dtypes[key])


filtered_data = pd.read_csv("filtered_data.csv", usecols=lambda x: x in dtypes.keys(),dtype=dtypes)
    
methods.createHistogram(filtered_data, "day_of_week")
methods.createPie(filtered_data, "number_of_game")
methods.createLinear(filtered_data, "day_of_week", "length_minutes")
methods.createBox(filtered_data, "number_of_game", "h_errors")
methods.createCorrelation(filtered_data, ["v_hits", "h_hits", "h_walks", "h_errors"])
