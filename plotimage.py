import numpy as np
import matplotlib.pyplot as plt

data = np.loadtxt(r'code\5.txt')
print(data.shape)

# 繪製圖片
plt.imshow(data, cmap='gray', vmin=0, vmax=128)
plt.colorbar()  
plt.show()


