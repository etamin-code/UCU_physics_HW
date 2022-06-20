from random import random
import matplotlib.pyplot as plt

from atoms import Cell
from system import System
from vectors import Vector

n = 100
dt = 0.00001
size = Vector(20, 20, 20)
N_max = 100

simulation = System({Cell(
    (float(random() * size.x), float(random() * size.y),
     float(random() * size.z)), (-1, -1, -1)) for _ in range(n)}, dt, size)
for i in range(N_max):
    print(f"epoch {i}/{N_max}")
    simulation.next_period_step()
print(simulation.U)
print(simulation.K)
print(simulation.W)

plt.plot(list(simulation.U.keys())[1:], list(simulation.U.values())[1:])
plt.xlabel("epochs")
plt.ylabel("U")
plt.show()

plt.plot(list(simulation.K.keys())[1:], list(simulation.K.values())[1:])
plt.xlabel("epochs")
plt.ylabel("K")
plt.show()

plt.plot(list(simulation.W.keys())[1:], list(simulation.W.values())[1:])
plt.xlabel("epochs")
plt.ylabel("W")
plt.show()

