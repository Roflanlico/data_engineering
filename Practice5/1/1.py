from pymongo import MongoClient
import json

def getColl(conUrl):
    client = MongoClient(conUrl)
    db = client["task1"]
    return db.person_data


#data = load_data("task_1_item.json")
file_js = open('task_1_item.json', "r", encoding="utf-8")
data = json.load(file_js)
file_js.close()
#print(data)
collection = getColl("mongodb://localhost:27017")

if collection.count_documents({}) == 0:
    collection.insert_many(data)

persons = list(collection.find({}).limit(10).sort({"salary": -1}))
with open("result_1_salary.json", "w", encoding="utf-8") as file:
    file.write(json.dumps(persons, ensure_ascii=False, default=str))

persons = list(collection.find({"age": {"$lt": 45}}, limit=15).sort({"salary": -1}))
with open("result_1_age.json", "w", encoding="utf-8") as file:
    file.write(json.dumps(persons, ensure_ascii=False, default=str))

query = {"city": "Куэнка", "job": {"$in": ["Учитель", "Повар", "Психолог"]}}
persons = list(collection.find(query, limit=10).sort({"age": 1}))
with open("result_1_city.json", "w", encoding="utf-8") as file:
    file.write(json.dumps(persons, ensure_ascii=False, default=str))

query = {
        "age": {"$gt": 30, "$lt": 45},
        "year": {"$in": [2019, 2020, 2021, 2022]},
        "$or": [{"salary": {"$gt": 50000, "$lte": 75000}},
                {"salary": {"$gt": 125000, "$lt": 150000}}]
    }
with open("result_1_complex.json", "w", encoding="utf-8") as file:
    file.write(json.dumps(len(list(collection.find(query))), ensure_ascii=False, default=str))
