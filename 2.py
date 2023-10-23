with open("text_2_var_70") as file:
    text = file.readlines()
result = []
for line in text:
    line = list(map(int, line.split(":")))
    result.append(sum(line))
with open('result_2.txt', 'w') as file:
    for elem in result:
        file.write(str(elem) + "\n")

