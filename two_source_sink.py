import numpy as np
import matplotlib.pyplot as plt

#defining mesh
x = np.linspace(-5, 5, 200)
y = np.linspace(-5, 5, 200)
X, Y = np.meshgrid(x, y)

#flow params
U = 1.5
Lambda1 = 2.0    #volume flow rate of source/sink №1
x1=2.5; y1=0     #coords of source/sink №1
Lambda2 = -2.0   #volume flow rate of source/sink №2
x2=-2.5; y2=0    #coords of source/sink №2

X_shifted1 = X - x1; Y_shifted1 = Y - y1
X_shifted2 = X - x2; Y_shifted2 = Y - y2

#cylindric coords
r1 = np.sqrt(X_shifted1**2 + Y_shifted1**2)
r1 = np.maximum(r1, 0.1)
theta1 = np.arctan2(Y_shifted1, X_shifted1 + 0.01)
r2 = np.sqrt(X_shifted2**2 + Y_shifted2**2)
r2 = np.maximum(r2, 0.1)
theta2 = np.arctan2(Y_shifted2, X_shifted2 + 0.01)

#flow functions
psi = np.zeros_like(X)
#psi += U * Y  
psi += (Lambda1 / (2 * np.pi)) * theta1      #source/sink №1
psi += (Lambda2 / (2 * np.pi)) * theta2      #source/sink №1

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
