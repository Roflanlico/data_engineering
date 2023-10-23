with open("text_3_var_70") as file:
    text = file.readlines()
with open('result_3.txt', 'w') as file:
    for line in text:    
        line = line.split(",")
        result = ""
        for i in range(len(line)):
            if line[i] == "NA":
                line[i] = (int(line[i-1]) + int(line[i + 1])) / 2
            if float(line[i]) ** 0.5 >= 70 + 50:
                result += str(line[i]) + ","
        result = result[:-1:]
        file.write(result)

