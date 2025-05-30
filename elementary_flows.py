import numpy as np
import matplotlib.pyplot as plt

#defining mesh
x = np.linspace(-5, 5, 200)
y = np.linspace(-5, 5, 200)
X, Y = np.meshgrid(x, y)

#flow params
U = 3.0          #uniform velocity rate
Lambda = 4.0     #volume flow rate
mu = 3.5
Gamma = 10.0

#cylindric coords
r = np.sqrt(X**2 + Y**2)
r = np.maximum(r, 0.1)  
theta = np.arctan2(Y, X)

#flow functions
psi = np.zeros_like(X)

psi += U * Y                               #uniform flow
#psi += (Lambda / (2 * np.pi)) * theta      #source/sink
#psi += (Gamma / (2 * np.pi)) * np.log(r)   #vortex
#psi += (-mu * Y) / (X ** 2 + Y **2)        #doublet

#visualization
plt.figure(figsize=(12, 10))
plt.contour(X, Y, psi, levels=30, colors='black', linewidths=1, linestyles='solid')
plt.title('Flow Visualization')
plt.xlabel('X')
plt.ylabel('Y')
plt.gca().set_aspect('equal')
plt.xlim(-5, 5)
plt.ylim(-5, 5)
plt.grid(True, linestyle=':', alpha=0.5)
plt.show()
