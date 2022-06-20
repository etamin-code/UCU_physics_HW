import numpy as np
import matplotlib.pyplot as plt


def count_U(sigma=1, epsilon=1, r=1):
    return 4 * epsilon * ((sigma/r)**12 - (sigma/r)**6)

sigma = 1
epsilon = 1
R = np.linspace(1, 5, 40)
U = count_U(r=R)

plt.plot(R, U)
plt.xlabel("r")
plt.ylabel("U")
plt.show()