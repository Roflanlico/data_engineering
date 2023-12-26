import os
import pandas as pd
from tqdm import tqdm
import numpy as np
import methods
import warnings
warnings.filterwarnings("ignore")



file_size = os.path.getsize("[2]automotive.csv.zip")
memory_usage = methods.getDataInfoChuncked("[2]automotive.csv.zip","memory_usage.json", chunksize=500_000)
print(f"Size without optimization: {memory_usage['file_in_memory_size']} MB")

dtypes = {'stockNum': pd.StringDtype(),'brandName': pd.CategoricalDtype(),'modelName': pd.CategoricalDtype(),'askPrice': pd.StringDtype(),'isNew': pd.CategoricalDtype(),'color': pd.CategoricalDtype(),'vf_Wheels': pd.StringDtype(),'vf_WheelSizeFront': pd.StringDtype(), 'vf_Windows': pd.StringDtype(),'vf_WheelSizeRear': pd.StringDtype() }

flag_header = True
size = 0
chunk = pd.read_csv("[2]automotive.csv.zip", usecols=lambda x: x in dtypes.keys(), dtype=dtypes,chunksize=500_000)
for elem in tqdm(chunk):
        size += elem.memory_usage(deep=True).sum()
        elem.dropna().to_csv("filtered_data.csv", mode="a", header=flag_header, index=False)
        flag_header = False

data = pd.read_csv("filtered_data.csv")
data_optimized = methods.optimizeData(data)
print(f"Memory size dataset with optimization: {data_optimized.memory_usage(deep=True).sum() // (1024**2)} MB")
methods.getDataInfo(data_optimized, file_size, "memory_usage.json")

dtypes = methods.saveData(data_optimized, dtypes.keys(), "data_optimized_dtype.json")
    
for key in dtypes.keys():
    if dtypes[key] == 'category':
        dtypes[key] = pd.CategoricalDtype
    else:
        dtypes[key] = np.dtype(dtypes[key])
print(dtypes)

print(data_optimized.info())
    
methods.createHistogram(data_optimized, "brandName")
methods.createPie(data_optimized, "isNew")
methods.createLinear(data_optimized, "brandName", "vf_Windows")
methods.createBox(data_optimized, "isNew", "askPrice")
methods.createCorrelation(data_optimized, ["askPrice", "vf_Wheels", "vf_WheelSizeFront", "vf_WheelSizeRear", "vf_Windows"])