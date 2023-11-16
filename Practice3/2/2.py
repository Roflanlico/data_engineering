import json
import zipfile
import os
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
            html_content = page.read()
        soup = BeautifulSoup(html_content, "html.parser")

        items = soup.find_all("div", attrs={"class": "product-item"})
            
        for item in items:
            id = item.a["data-id"]
            href = item.find_all("a")[1]["href"]
            img_src = item.find_all("img")[0]["src"]
            name = item.find_all("span")[0].get_text().strip()
            
            price = int(item.find_all("price")[0].get_text().replace("₽", "").replace(" ", "").strip())
            if price >= max_price:
                max_price = price
            if price <= min_price:
                min_price = price
            sum_price += price
            counter+=1
            
            bonus = item.find_all("strong")[0].get_text().replace("+ начислим", "").replace("бонусов", "").strip()

            info = {}
            props = item.find_all("li")
            for prop in props:
                freq[prop["type"]] = freq.get(prop["type"], 0) + 1    
                info[prop["type"]] = prop.get_text().strip()
        
            product = {
                "Id": id,
                "Href": href,
                "Img_src": img_src,
                "Name": name,
                "Price": price,
                "Bonus": bonus,
                "Info": info,
            }
            data.append(product)


with open("result_2.json", "w") as file:
    file.write(json.dumps(data, indent=2, ensure_ascii=False))
    
sorted_data = sorted(data, key=lambda x: x["Id"])
filtered_data = list(filter(lambda x: x["Price"] >= 100000, data))

with open("result_sorted_2.json", "w") as file:
    file.write(json.dumps(sorted_data, indent=2, ensure_ascii=False))

with open("result_filtered_2.json", "w") as file:
    file.write(json.dumps(filtered_data, indent=2, ensure_ascii=False))

avg_price = sum_price / counter

with open("stats_2.json", "w") as file:
    file.write(json.dumps(
            {
                "Sum": sum_price,
                "min": min_price,
                "max": max_price,
                "average": avg_price
            },
            indent=2))
    
freq_sorted = dict(sorted(freq.items(), key=lambda x: x[1], reverse=True))

with open("freq_2.json", "w", encoding="utf-8") as file:
    file.write(json.dumps(freq_sorted, ensure_ascii=False, indent=2))
