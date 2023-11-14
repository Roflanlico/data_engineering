import pickle
import json

file = open("products_70.pkl", "rb")
products = pickle.load(file)
file.close()

file = open("price_info_70.json", "r")
prices_info = json.load(file)
file.close()   

prices_info_dict = {}

for item in prices_info:
    prices_info_dict[item["name"]] = item

for product in products:
    current_price_info = prices_info_dict[product["name"]]
    
    method = current_price_info["method"]
    if method == "sum":
        product["price"] = round(product["price"] + current_price_info["param"],2)
    elif method == "sub":
        product["price"] = round(product["price"] - current_price_info["param"],2)
    elif method == "percent+":
        product["price"] = round(product["price"] * (1 + current_price_info["param"]),2)
    elif method == "percent-":
        product["price"] = round(product["price"] * (1 - current_price_info["param"]),2)

file = open("result_4.pkl", "wb")
pickle.dump(products, file)
file.close()
