import numpy as np
import matplotlib.pyplot as plt

x = np.array([0,1,2,3])
y = np.exp(x)

plt.figure()
plt.plot(x,y)
plt.show()