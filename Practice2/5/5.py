import pandas as pd
import msgpack
import json
import os

result = dict()
data = pd.read_csv('organizations-500000.csv')

dataframe = pd.DataFrame(data)
dataframe.to_json('organizations-500000.json')
dataframe.to_pickle('organizations-500000.pkl')
file = open('organizations-500000', 'wb')
file.write(msgpack.packb(dataframe.to_dict()))
file.close()

num = ['Founded','Number of employees']
lit = ['Name', 'Country', 'Industry']

def procNums(result, data, fields):
  for field in fields:
    result[field] = {
      'MAX': data[field].max(),
      'MIN': data[field].min(),
      'AVG': data[field].mean(),
      'SUM': data[field].sum(),
      'STD': data[field].std(),
      'FRQ': "Only for literal value"
    }

def procLits(result, data, fields):
  for field in fields:
    result[field] = {
      'MAX': "Only for numeric value",
      'MIN': "Only for numeric value",
      'AVG': "Only for numeric value",
      'SUM': "Only for numeric value",
      'STD': "Only for numeric value",
      'FRQ': data[field].value_counts().to_dict()
    }
procNums(result, data, num)
procLits(result, data, lit)

df = pd.DataFrame(result)
df.to_json('result_5.json')



print("Размер json файла: " + str(os.path.getsize('organizations-500000.json')))
print("Размер csv файла: " + str(os.path.getsize('organizations-500000.csv')))
print("Размер pkl файла: " + str(os.path.getsize('organizations-500000.pkl')))
print("Размер msgpack файла: " + str(os.path.getsize('organizations-500000.msgpack')))
