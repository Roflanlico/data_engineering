import numpy as np
import json

matrix = np.load('matrix_70.npy')
print(matrix)

np.save('matrix_normilized.npy', matrix/int(np.sum(matrix)))

result = {
    "sum": int(np.sum(matrix)),
    "avr": float(np.mean(matrix)),
    "sumMd": int(np.trace(matrix)),
    "avrMD": float(np.mean(np.diagonal(matrix))),
    "sumSD": int(np.trace(np.fliplr(matrix))),
    "avrSD": float(np.mean(np.fliplr(matrix).diagonal())),
    "max": int(np.max(matrix)),
    "min": int(np.min(matrix))
}

with open('result_1.json', 'w') as file:
    json.dump(result, file, indent=4)
