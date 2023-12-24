from pymongo import MongoClient

def getColl(conUrl):
    client = MongoClient(conUrl)
    db = client["task1"]
    return db.person_data

def loadTextData(fileName):
    with open(fileName, "r", encoding="utf-8") as file:
       lines = file.readlines()
    data = []
    obj = {}
    for line in lines:
        if line.strip() != "=====":
            s = line.strip().split("::")
            obj[s[0]] = int(s[1]) if s[1].isdigit() else s[1]
        else:
            data.append(obj)
            obj = {}
    return data

#with open("task_3_item.msgpack", "rb") as data_file:
#    byte_data = data_file.read()
#data = msgpack.unpackb(byte_data)

data = loadTextData('task_3_item.text')

collection = getColl("mongodb://localhost:27017")
collection.insert_many(data)

query = {"$or": [{"salary": {"$lt": 25000}},{"salary": {"$gt": 175000}}]}
collection.delete_many(query)

collection.update_many({}, {"$inc": {"age": 1}})

collection.update_many({"job": {"$in": ["Повар"]}},{"$mul": {"salary": 1.05}})

collection.update_many({"city": {"$in": ["Тбилиси"]}},{"$mul": {"salary": 1.07}})

collection.update_many({"$and": [{"city": {"$in": ["Москва"]}},{"job": {"$in": ["Учитель"]}}]},{"$mul": {"salary": 1.10}})

collection.delete_many({"job": "IT-специалист"})
