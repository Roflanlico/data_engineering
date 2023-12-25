import json
import zipfile
import os
import urllib.request
from bs4 import BeautifulSoup

data = list()
data2 = list()
score_max = 0
score_min = 10.0
score_avg = 0
score_sum = 0

counter = 0
freq = {}

url = "https://shikimori.one/animes"

user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'
headers={'User-Agent':user_agent,}




def parse_page(data, url, headers):
    for i in range(3): 
      request=urllib.request.Request(url,None,headers) #The assembled request
 
      html_content = urllib.request.urlopen(request).read() 
  
      soup = BeautifulSoup(html_content, "html.parser")
  
      items = soup.find_all("article", class_=['c-anime'])
            
      for item in items:
        if len(item.find_all("a", class_=['cover'])) > 0:
            href = item.find_all("a", class_=['cover'])[0].get('href')

        name = item.find_all("span", class_=['name-ru'])[0].get_text()

        type = item.find_all("span", class_=['misc'])[0].find_all('span')[0].get_text()

        year = item.find_all("span", class_=['misc'])[0].find_all('span')[1].get_text()
    
        anime = {
        "Href": href,
        "Name": name,
        "Type": type,
        "Production year": int(year),
        }
        data.append(anime)
        next = soup.find_all('a', class_=['next'])[0].get('href')
        url = next

parse_page(data, url, headers)

print(data)
            
for anime in data:
    link = anime['Href']
    request=urllib.request.Request(link,None,headers) #The assembled request
 
    html_content = urllib.request.urlopen(request).read() 
  
    soup = BeautifulSoup(html_content, "html.parser")

    name = soup.find_all('h1')[0].get_text().strip()
    
    
    type = soup.find_all('div', class_=['value'])[0].get_text().strip()
    amount = soup.find_all('div', class_=['value'])[1].get_text().strip()
    genres = ' '.join(x.get_text().strip() for x in soup.find_all("span", class_=['genre-ru'])).strip()
    rating = soup.find_all('div', class_=['value'])[5].get_text().strip()
    score = soup.find_all('div', class_=['score-value'])[0].get_text().strip()
    
    anime_info = {
        "Name": name,
        "Type": type,
        "Episodes amount": amount,
        "Genres": genres,
        "Age rating": rating,
        "Score": float(score),
    }
    data2.append(anime_info)

for anime in data2:
    cur = anime['Score']
    score_max = score_max if cur < score_max else cur
    score_min = score_min if score_min < cur else cur
    counter += 1
    score_sum += cur

score_avg = score_sum / counter

for anime in data2:
    curr = anime['Genres'].split()
    for e in curr:
        freq[e] = freq.get(e, 0) + 1

with open("result_5.json", "w") as file:
    file.write(json.dumps(data, indent=2, ensure_ascii=False))
    
sorted_data = sorted(data, key=lambda x: x["Type"])
filtered_data = list(filter(lambda x: x["Production year"] >= 2000, data))

with open("result_sorted_5.json", "w") as file:
    file.write(json.dumps(sorted_data, indent=2, ensure_ascii=False))

with open("result_filtered_5.json", "w") as file:
    file.write(json.dumps(filtered_data, indent=2, ensure_ascii=False))



with open("stats_5.json", "w") as file:
    file.write(json.dumps(
            {
                "Sum": score_sum,
                "min": score_min,
                "max": score_max,
                "average": score_avg,
            },
            indent=2))
    
freq_sorted = dict(sorted(freq.items(), key=lambda x: x[1], reverse=True))

with open("t5_freq.json", "w", encoding="utf-8") as file:
    file.write(json.dumps(freq_sorted, ensure_ascii=False, indent=2))
