import os
import json
import zipfile
from bs4 import BeautifulSoup

data = list()
max_price = 0
min_price = 99999999
avg_price = 0
sum_price = 0

counter = 0
freq = {}

with zipfile.ZipFile("zip_var_70.zip", "r") as file:
    files = file.namelist()
    for filename in files:
        with file.open(filename) as page:
            soup = BeautifulSoup(page, 'xml')
            
            clothings = soup.find_all("clothing")
            for clothing in clothings:
                item = {}
                for elem in clothing.contents:
                    if elem.name is not None:
                        try:
                            item[elem.name] = float(elem.get_text().strip())
                            if elem.name == "price":
                                price = float(elem.get_text().strip())
                                if price >= max_price:
                                    max_price = price
                                if price <= min_price:
                                    min_price = price
                                sum_price += price
                                counter += 1
                        except:
                            item[elem.name] = elem.get_text().strip()
                            if elem.name == "category":
                                freq[elem.get_text().strip()] = freq.get(elem.get_text().strip(), 0) + 1
                data.append(item)
            
with open("result_4.json", "w") as file:
    file.write(json.dumps(data, indent=2, ensure_ascii=False))
    
sorted_data = sorted(data, key=lambda x: x["rating"])
filtered_data = list(filter(lambda x: x["price"] >= 700000, data))

with open("result_sorted_4.json", "w") as file:
    file.write(json.dumps(sorted_data, indent=2, ensure_ascii=False))

with open("result_filtered_4.json", "w") as file:
    file.write(json.dumps(filtered_data, indent=2, ensure_ascii=False))

avg_price = sum_price / counter

with open("stats_4.json", "w") as file:
    file.write(json.dumps(
            {
                "Sum": sum_price,
                "min": min_price,
                "max": max_price,
                "average": avg_price
            },
            indent=2))
    
freq_sorted = dict(sorted(freq.items(), key=lambda x: x[1], reverse=True))

with open("freq_4.json", "w", encoding="utf-8") as file:
    file.write(json.dumps(freq_sorted, ensure_ascii=False, indent=2))