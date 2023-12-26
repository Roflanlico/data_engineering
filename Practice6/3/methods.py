import os
import json
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from tqdm import tqdm


def getDataInfo(data, file_size, result_file):
    memory_usage = data.memory_usage(deep=True)
    memory_usage_overall = float(memory_usage.sum())
    columns = {}

    for column in data:
        columns[column] = {
            'total_memory': float(memory_usage[column]) // 1024,
            'memory_space_percentage': round(memory_usage[column] / memory_usage_overall * 100, 2),
            'dtype': str(data.dtypes[column])
        }
    
    columns = dict(sorted(list(columns.items()), key=lambda x: x[1]['total_memory'], reverse=True))
    results = {
        'file_size': file_size // 1024, # KB
        'file_in_memory_size': memory_usage_overall // 1024, # KB
        'columns_stats': columns
    }
    with open(result_file, "w") as file:
        json.dump(results, file, ensure_ascii=False )
        
    return results

def getDataInfoChuncked(path_to_file, result_file, chunksize):
    file_size = os.path.getsize(path_to_file)
    memory_usage_overall = 0
    data = pd.read_csv(path_to_file, chunksize=chunksize)  
    columns = {}
    for chunk in tqdm(data):
        chunk_memory_usage_stat = chunk.memory_usage(deep=True)
        memory_usage_overall += float(chunk_memory_usage_stat.sum())
        for column in chunk:
            if column in columns:
                columns[column]['total_memory'] += float(chunk_memory_usage_stat[column])
            else:
                columns[column] = {
                    'total_memory': float(chunk_memory_usage_stat[column]),
                    'dtype': str(chunk.dtypes[column])
                }    
    for column in columns.keys():
        columns[column]['memory_space_percentage'] = round(columns[column]['total_memory'] / memory_usage_overall * 100, 2)
        columns[column]['total_memory'] = columns[column]['total_memory'] // 1024
    
    columns = dict(sorted(list(columns.items()), key=lambda x: x[1]['total_memory'], reverse=True))
    results = {
        'file_size': file_size // 1024,
        'file_in_memory_size': memory_usage_overall // 1024,
        'columns_stats': columns
    }
    
    with open(result_file, "w", encoding='utf-8') as file:
        json.dump(results, file, ensure_ascii=False)

    return results

def optimizeData(data):
    for column in data.select_dtypes(include=['object']):
        length = len(data[column])
        uniqueLength = len(data[column].unique())
        if uniqueLength / length < 0.5:
            data[column] = data[column].astype('category')
            
    for column in data.select_dtypes(include=['int']): 
        if False not in set(data[column] >= 0):
            data[column] = pd.to_numeric(data[column], downcast='unsigned')
        else:
            data[column] = pd.to_numeric(data[column], downcast='signed')
            
    for column in data.select_dtypes(include=['float']):
        data[column] = pd.to_numeric(data[column], downcast='float')
    
    return data

def saveData(data, columns, file_save):
    newData = {column_name: data[column_name].dtype.name for column_name in columns}

    with open(file_save, "w", encoding='utf-8') as file:
        json.dump(newData, file, ensure_ascii=False)
        
    return newData

def createLinear(data, droup, column):
    plt.figure(figsize=(30,15))
    plt.plot(data.groupby([droup])[column].sum().values, marker='*', color='red')
    plt.xlabel(droup)
    plt.ylabel(column)
    plt.savefig("linear_graphics.jpg")
    plt.close()

def createHistogram(data, column):
    plt.figure(figsize=(30,15))
    plot = data[column].hist(grid=False, edgecolor='black')
    plt.xlabel(column)
    plot.get_figure().savefig("histogram.jpg")
    plt.close()

def createPie(data, column):
    plt.figure()
    groups = data.groupby([column])[column].count()
    circ = groups.plot(kind='pie', y=groups.keys(), autopct='%1.0f%%')
    circ.get_figure().savefig("pie.jpg")
    plt.close()

def createCorrelation(df, columns):
    data = df.copy()
    plt.figure(figsize=(16,16))
    plot = sns.heatmap(data[columns].corr())
    plot.get_figure().savefig("correlation.jpg")
    plt.close()
    
def createBox(data, c1, c2):
    plt.figure(figsize=(30,15))
    plot = sns.boxplot(data=data, x=c1, y=c2)
    plot.get_figure().savefig("box.jpg")
    plt.close()