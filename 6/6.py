import requests
import json

data = json.loads(requests.get(f"https://restcountries.com/v3.1/name/japan").text)[0]

HTML_TEMPLATE = f"""<!doctype html>
<html lang="ru">
<head>
<meta charset="utf-8" />
<title></title>
<link rel="stylesheet" href="style.css" />
</head>
<body>
<h1>Страна {data['name']['common']}</h1>
<p>Регион: {data['region']}</p>
<p>Столица: {data['capital'][0]}</p>
<p>Площадь: {data['area']}</p>
</body>
</html>
"""


# Запись вывода в HTML файл
with open("japan.html", "w", encoding='utf-8', newline="") as file:
    file.write(HTML_TEMPLATE)
