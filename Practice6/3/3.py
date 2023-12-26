import os
import pandas as pd
from tqdm import tqdm
import numpy as np
import methods
import warnings
warnings.filterwarnings("ignore")

 
file_size = os.path.getsize("[3]flights.csv")
memory_usage = methods.getDataInfoChuncked("[3]flights.csv","memory_usage.json", chunksize=500_000)
print(f"Size without optimization: {memory_usage['file_in_memory_size']} MB")

dtypes = {'YEAR': pd.StringDtype(),'MONTH': pd.StringDtype(),'DAY': pd.StringDtype(),'DAY_OF_WEEK': pd.StringDtype(),'AIRLINE': pd.CategoricalDtype(),'TAIL_NUMBER': pd.CategoricalDtype(),'FLIGHT_NUMBER': pd.StringDtype(),'SCHEDULED_DEPARTURE': pd.StringDtype(), 'DEPARTURE_TIME': pd.StringDtype(),'DEPARTURE_DELAY': pd.StringDtype() }

flag_header = True
size = 0
chunk = pd.read_csv("[3]flights.csv", usecols=lambda x: x in dtypes.keys(), dtype=dtypes,chunksize=500_000)
for elem in tqdm(chunk):
        size += elem.memory_usage(deep=True).sum()
        elem.dropna().to_csv("filtered_data.csv", mode="a", header=flag_header, index=False)
        flag_header = False

data = pd.read_csv("filtered_data.csv")
df_optimize = methods.optimizeData(data)
print(f"Memory size dataset with optimization: {df_optimize.memory_usage(deep=True).sum() // (1024**2)} MB")
methods.getDataInfo(df_optimize, file_size, "memory_usage.json")

dtypes = methods.saveData(df_optimize, dtypes.keys(), "data_optimized_dtype.json")
    
for key in dtypes.keys():
    if dtypes[key] == 'category':
        dtypes[key] = pd.CategoricalDtype
    else:
        dtypes[key] = np.dtype(dtypes[key])

print(df_optimize.info())

methods.createHistogram(df_optimize, "MONTH")
methods.createPie(df_optimize, "AIRLINE")
methods.createLinear(df_optimize, "MONTH", "DEPARTURE_DELAY")
methods.createBox(df_optimize, "AIRLINE", "FLIGHT_NUMBER")
methods.createCorrelation(df_optimize, ["DAY_OF_WEEK", "SCHEDULED_DEPARTURE", "DEPARTURE_DELAY", "DEPARTURE_TIME", "FLIGHT_NUMBER"]) 