
import matplotlib.pyplot as plt

ph = [6.2, 6.8, 7.2, 7.8, 8.4]
r = [246, 238, 229, 233, 247]
g = [172, 107, 58, 29, 2]
b = [2, 1, 1, 5, 28]

plt.plot(ph, r, color='red')
plt.plot(ph, g, color='green')
plt.plot(ph, b, color='blue')

plt.show()

