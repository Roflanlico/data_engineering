import csv
with open('text_4_var_70', 'rt', encoding='utf-8') as file:
    with open('result_4', 'w', encoding='utf-8') as file_result:
        s = 0
        count = 0
        result = []
        for e in csv.reader(file, delimiter=','):
            s += int(e[4].replace("₽",""))
            count += 1
            result.append([e[i] for i in range(5)])
        avg = s / count
        result.sort(key = lambda item: item[0])
        for x in result:
            if int(x[4].replace("₽","")) >= avg and int(x[0]) > 25 + (70 % 10):
                csv.writer(file_result).writerow(x)
