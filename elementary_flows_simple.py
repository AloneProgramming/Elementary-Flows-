import numpy as np
import matplotlib.pyplot as plt

# defining grid
x = np.linspace(-5, 5, 200)
y = np.linspace(-5, 5, 200)
X, Y = np.meshgrid(x, y)

# setting flow params
U = 100.0         # uniform flow rate
Lambda = 75.0     # source/sink volume flow rate
mu = 1.5          # doublet volume flow rate
Gamma = 5.0       # vortex circulation rate
p0 = 101325.0     # free stream pressure
rho = 1.225       # fluid density

# defining fields
psi = np.zeros_like(X)
u = np.zeros_like(X)
v = np.zeros_like(X)

# division-by-zero protection
r_sq = X**2 + Y**2
r_sq = np.where(r_sq < 1e-10, 1e-10, r_sq)  
r = np.sqrt(r_sq)
theta = np.arctan2(Y, X)

# flow functions
def uniform_flow(U):
    u = U * np.ones_like(X)
    v = np.zeros_like(X)
    psi = U * Y
    return u, v, psi

def source_sink(Lambda):
    u = (Lambda / (2 * np.pi)) * X / r_sq
    v = (Lambda / (2 * np.pi)) * Y / r_sq
    psi = (Lambda / (2 * np.pi)) * theta
    return u, v, psi

def vortex(Gamma):
    u = (Gamma / (2 * np.pi)) * Y / r_sq
    v = (Gamma / (2 * np.pi)) * (-X) / r_sq
    psi = (Gamma / (2 * np.pi)) * np.log(r)
    return u, v, psi

def doublet(mu):
    u = (-mu / r_sq) * (1 - 2 * (X**2) / r_sq)
    v = (-mu / r_sq) * (-2 * X * Y / r_sq)
    psi = (-mu * Y) / r_sq
    return u, v, psi

# flow superposition (uncomment ones you need)
components = [
    uniform_flow(U),
    # source_sink(Lambda),
    vortex(Gamma),
    # doublet(mu)
]

for comp in components:
    u_comp, v_comp, psi_comp = comp
    u += u_comp
    v += v_comp
    psi += psi_comp

speed = np.sqrt(u**2 + v**2)
pressure = p0 + 0.5 * rho * (U**2 - speed**2)

# visualization
plt.figure(figsize=(14, 10))

# velocity potential
speed_plot = plt.pcolormesh(
    X, Y, speed,
    cmap='jet',         
    shading='auto',     
    vmin=0,             
    vmax=speed.max()    
)
# plt.colorbar(speed_plot, label='Speed', shrink=0.8)

#pressure distribution
pressure_plot = plt.pcolormesh(
    X, Y, pressure,
    cmap='jet',         
    shading='auto',     
    vmin=pressure.min(),             
    vmax=pressure.max()    
)
plt.colorbar(pressure_plot, label='Pressure', shrink=0.8)

# stream function
streamlines = plt.contour(
    X, Y, psi,
    levels=30,          # change number to make lines denser
    colors='black',     
    linewidths=0.8,     
    linestyles='solid'  
)

plt.title('Flow Visualization')
plt.xlabel('X')
plt.ylabel('Y')
plt.gca().set_aspect('equal')
plt.xlim(-5, 5)
plt.ylim(-5, 5)
plt.grid(True, linestyle=':', alpha=0.5)
plt.tight_layout()
plt.show()