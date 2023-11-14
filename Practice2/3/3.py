import json
import msgpack
import os

file = open('products_70.json')
json_data = json.load(file)
file.close()

result = {}
for item in json_data:
    name = item["name"]
    price = item["price"]
    if name in result:
        data = result[name]
        data["count"] += 1
        data["sum"] += price
        data["average_price"] = (data["sum"]) / data["count"]
        data["max_price"] = max(data["max_price"], price)
        data["min_price"] = min(data["min_price"], price)
    else:
        result[name] = {"average_price": price, "max_price": price, "min_price": price, "count": 1, "sum": price}

file = open("result_3.json", "w")
json.dump([{"name": name, **data} for name, data in result.items()], file, indent=2)
file.close()

file = open("result_3.msgpack", "wb")
file.write(msgpack.packb(result))
file.close()

print("Размер оригинального файла: " + str(os.path.getsize('result_3.json')))
print("Размер сжатого файла: " + str(os.path.getsize('result_3.msgpack')))
