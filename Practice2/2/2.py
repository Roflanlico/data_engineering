import numpy as np
import os

matrix = np.load('matrix_70_2.npy')
x, y = np.where(matrix > 570 )
z = matrix[matrix > 570]
np.savez('result_2.npz', x=x, y=y, z=z)
np.savez_compressed('result_2_compressed.npz', x=x, y=y, z=z)

print("Размер оригинального файла: " + str(os.path.getsize('result_2.npz')))
print("Размер сжатого файла: " + str(os.path.getsize('result_2_compressed.npz')))
