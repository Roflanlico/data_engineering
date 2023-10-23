with open("C:/Users/R/Documents/Python/Practice1/1/text_1_var_70") as file:
    text = file.readlines()
frequency = {}
punctuation = [".", ",", "!", "?",":",";"]
for line in text:
    for s in punctuation:
        line = line.replace(s," ")
    line = line.split()
    for e in line:
        if e in frequency:
            frequency[e] += 1
        else:
            frequency[e] = 1
frequency = sorted(frequency.items(), key=lambda item: item[1], reverse=True)
with open('C:/Users/R/Documents/Python/Practice1/1/result_1.txt', 'w') as file:
    for key, value in frequency:
        file.write(f'{key}:{value}\n')
