import os
import pandas as pd
from tqdm import tqdm
import numpy as np
import methods
import warnings
warnings.filterwarnings("ignore")

file_name = "[4]vacancies.csv.gz"    
file_size = os.path.getsize(file_name)
memory_usage = methods.getDataInfoChuncked(file_name,"memory_usage.json", chunksize=500_000)
print(f"Size without optimization: {memory_usage['file_in_memory_size']} MB")

dtypes = {'id': pd.StringDtype(),'prof_classes_found': pd.StringDtype(),'key_skills': pd.StringDtype(),'address_city': pd.CategoricalDtype(),'schedule_id': pd.CategoricalDtype(), 'address_lng': pd.StringDtype(),'address_lat': pd.StringDtype(),'salary_from': pd.StringDtype(),'salary_to': pd.StringDtype(),'employment_name': pd.CategoricalDtype(),}

flag_header = True
size = 0
chunk = pd.read_csv(file_name, usecols=lambda x: x in dtypes.keys(), dtype=dtypes,chunksize=500_000)
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

print(data_optimized.info())

methods.createHistogram(data_optimized, "prof_classes_found")
methods.createPie(data_optimized, "employment_name")
methods.createLinear(data_optimized, "salary_from", "salary_to")
methods.createBox(data_optimized, "schedule_id", "salary_to")
methods.createCorrelation(data_optimized, ["salary_from", "salary_to", "address_lat", "address_lng"])