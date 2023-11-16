import os
import json
import zipfile
from bs4 import BeautifulSoup

data = list()
max_age = 0
min_age = 99999999
avg_age = 0
sum_age = 0

counter = 0
freq = {}

with zipfile.ZipFile("zip_var_70.zip", "r") as file:
    files = file.namelist()
    for filename in files:
        with file.open(filename) as page:
            soup = BeautifulSoup(page, 'xml')
            
            name = soup.find_all("name")[0].get_text().strip()
            constellation = soup.find_all("constellation")[0].get_text().strip()
            
            spectral_class = soup.find_all("spectral-class")[0].get_text().strip()
            freq[spectral_class] = freq.get(spectral_class, 0) + 1
            
            radius = float(soup.find_all("radius")[0].get_text().strip())
            rotation = float(soup.find_all("rotation")[0].get_text().replace("days", "").strip())
            
            age = float(soup.find_all("age")[0].get_text().replace("billion years", "").strip())
            if age >= max_age:
                max_age = age
            if age <= min_age:
                min_age = age
            sum_age += age
            counter+=1
            
            distance = float(soup.find_all("distance")[0].get_text().replace("million km", "").strip())
            absolute_magnitude = float(soup.find_all("absolute-magnitude")[0].get_text().replace("million km", "").strip())
            
        
        
            star = {
                "Name": name,
                "Constellation": constellation,
                "Spectral_class": spectral_class,
                "Radius": radius,
                "Rotation": rotation,
                "Age": age,
                "Distance": distance,
                "Absolute_magnitude": absolute_magnitude
            }
            data.append(star)


with open("result_3.json", "w") as file:
    file.write(json.dumps(data, indent=2, ensure_ascii=False))
    
sorted_data = sorted(data, key=lambda x: x["Radius"])
filtered_data = list(filter(lambda x: x["Age"] >= 2, data))

with open("result_sorted_3.json", "w") as file:
    file.write(json.dumps(sorted_data, indent=2, ensure_ascii=False))

with open("result_filtered_3.json", "w") as file:
    file.write(json.dumps(filtered_data, indent=2, ensure_ascii=False))

avg_age = sum_age / counter

with open("stats_3.json", "w") as file:
    file.write(json.dumps(
            {
                "Sum": sum_age,
                "min": min_age,
                "max": max_age,
                "average": avg_age
            },
            indent=2))
    
freq_sorted = dict(sorted(freq.items(), key=lambda x: x[1], reverse=True))

with open("freq_3.json", "w", encoding="utf-8") as file:
    file.write(json.dumps(freq_sorted, ensure_ascii=False, indent=2))
