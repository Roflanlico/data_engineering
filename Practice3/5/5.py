import json
import zipfile
import os
import urllib.request
from bs4 import BeautifulSoup

data = list()
price_max = 0
price_min = 999999999
price_avg = 0
price_sum = 0

counter = 0
freq = {}

url = "https://ulyanovsk.tur-region.ru/tours/avtobusnye-tury-na-chernoe-more"

for i in range(1): 
  html_content = urllib.request.urlopen(url ).read() 

  soup = BeautifulSoup(html_content, "html.parser")
  
  items = soup.find_all("div", attrs={"class": "tour__item"})
            
  for item in items:
    href = item.find_all("a", attrs={"tour__item-link"})[0]["href"]

    name = item.find_all("div", attrs={"tour__item-title"})[0].get_text().strip()

    
    #print(item.find_all("div", attrs={"tour__item-info"})[0].get_text().split(", \n        "))

    price = item.find_all("div", attrs={"tour__item-info"})[0].get_text().split(", \n        ")[0].replace("от", "").replace("руб.", "").replace(" ", "").strip()
    if price != "":
       price = float(price)
    else:
       price = 0
    if price >= price_max:
      price_max = price
    if price <= price_min:
      price_min = price
    price_sum += price
    counter+=1

    time = item.find_all("div", attrs={"tour__item-info"})[1].get_text().split(", \n        ")[0].replace("дней на море", "").strip()
        
    tour = {
        "Href": href,
        "Name": name,
        "Price": price,
        "Time amount": time,


        
        }
    data.append(tour)
            

with open("result_5.json", "w") as file:
    file.write(json.dumps(data, indent=2, ensure_ascii=False))
    
sorted_data = sorted(data, key=lambda x: x["Time amount"])
filtered_data = list(filter(lambda x: x["Price"] >= 15000, data))

with open("result_sorted_5.json", "w") as file:
    file.write(json.dumps(sorted_data, indent=2, ensure_ascii=False))

with open("result_filtered_5.json", "w") as file:
    file.write(json.dumps(filtered_data, indent=2, ensure_ascii=False))

price_avg = price_sum / counter

with open("stats_5.json", "w") as file:
    file.write(json.dumps(
            {
                "Sum": price_sum,
                "min": price_min,
                "max": price_max,
                "average": price_avg
            },
            indent=2))
    
freq_sorted = dict(sorted(freq.items(), key=lambda x: x[1], reverse=True))

with open("t5_freq.json", "w", encoding="utf-8") as file:
    file.write(json.dumps(freq_sorted, ensure_ascii=False, indent=2))
