import json
import zipfile
import os
import urllib.request
from bs4 import BeautifulSoup

data = list()
data2 = list()
price_max = 0
price_min = 999999999
price_avg = 0
price_sum = 0

counter = 0
freq = {}

url = "https://shikimori.one/animes"

user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7' 
headers={'User-Agent':user_agent,}



for i in range(3): 
  request=urllib.request.Request(url,None,headers) #The assembled request
 
  html_content = urllib.request.urlopen(request).read() 
  print(html_content)
  soup = BeautifulSoup(html_content, "html.parser")
  
  items = soup.find_all("div", class_=['c-anime'])
            
  for item in items:
    href = item.find_all("a", class_=['cover'])["href"]

    name = item.find_all("span", class_=['name-ru'])

    type = item.find_all("span", class_=['misc'])['span']

    year = item.find_all("span", class_=['misc'])['span']
    
    anime = {
        "Href": href,
        "Name": name,
        "Type": type,
        "Production year": year,
        }
    data.append(anime)
            
print(data)
with open("result_5.json", "w") as file:
    file.write(json.dumps(data, indent=2, ensure_ascii=False))
    
sorted_data = sorted(data, key=lambda x: x["Time amount"])
filtered_data = list(filter(lambda x: x["Price"] >= 15000, data))

with open("result_sorted_5.json", "w", encoding='utf-8') as file:
    file.write(json.dumps(sorted_data, indent=2, ensure_ascii=False))

with open("result_filtered_5.json", "w", encoding='utf-8') as file:
    file.write(json.dumps(filtered_data, indent=2, ensure_ascii=False))



with open("stats_5.json", "w", encoding='utf-8') as file:
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
