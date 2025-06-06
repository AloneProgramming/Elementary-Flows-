import numpy as np
import matplotlib.pyplot as plt

class FlowComponent:
    def __init__(self, strength, dx = 0, dy = 0):
        self.strength = strength
        self.dx = dx
        self.dy = dy

    def velocity_field(self, X, Y):
        return np.zeros_like(X), np.zeros_like(Y)
    
    def stream_function(self, X):
        return np.zeros_like(X) 
    
    def _shifted_coordinates(self, X, Y):
        return X - self.dx, Y - self.dy
    
class UniformFlow(FlowComponent):
    def __init__(self, strength, alpha=0, dx = 0, dy = 0):
        super().__init__(self, dx, dy)
        self.strength = strength
        self.alpha = alpha

    def velocity_field(self, X, Y):
        u = self.strength * np.cos(self.alpha)
        v = self.strength * np.sin(self.alpha)
        return u * np.ones_like(X), v * np.ones_like(Y)
    
    def stream_function(self, X, Y):
        return self.strength * (Y * np.cos(self.alpha) - X * np.sin(self.alpha))
    
class SourceSink(FlowComponent):
    def velocity_field(self, X, Y):
        X_shifted, Y_shifted = self._shifted_coordinates(X, Y)
        r_sq = np.maximum(X_shifted**2 + Y_shifted**2, 1e-10)  
        u = (self.strength / (2 * np.pi)) * X_shifted / r_sq
        v = (self.strength / (2 * np.pi)) * Y_shifted / r_sq
        return u, v
    
    def stream_function(self, X, Y):
        X_shifted, Y_shifted = self._shifted_coordinates(X, Y)
        return (self.strength / (2 * np.pi)) * np.arctan2(Y_shifted, X_shifted)
    
class Vortex(FlowComponent):
    def velocity_field(self, X, Y):
        X_shifted, Y_shifted = self._shifted_coordinates(X, Y)  
        r_sq = np.maximum(X_shifted**2 + Y_shifted**2, 1e-10)  
        u = (self.strength / (2 * np.pi)) * Y_shifted / r_sq
        v = (self.strength / (2 * np.pi)) * (-X_shifted) / r_sq
        return u, v
    
    def stream_function(self, X, Y):
        X_shifted, Y_shifted = self._shifted_coordinates(X, Y)
        r = np.sqrt(np.maximum(X_shifted**2 + Y_shifted**2, 1e-10))
        return (self.strength / (2 * np.pi)) * np.log(r)
    
class Doublet(FlowComponent):
    def velocity_field(self, X, Y):
        X_shifted, Y_shifted = self._shifted_coordinates(X, Y)  
        r_sq = np.maximum(X_shifted**2 + Y_shifted**2, 1e-10)  
        factor = self.strength / r_sq**2
        u = factor * (X_shifted**2 - Y_shifted**2)
        v = factor * (2 * X_shifted * Y_shifted)
        return u, v
    
    def stream_function(self, X, Y):
        X_shifted, Y_shifted = self._shifted_coordinates(X, Y)
        r_sq = np.maximum(X_shifted**2 + Y_shifted**2, 1e-10)  
        return (-self.strength * Y_shifted) * r_sq

class FlowModel:
    def __init__(self, components = None):
        self.components = components if components is not None else []

    def add_component(self, component):
        self.components.append(component)

    def velocity_field(self, X, Y):
        u_total = np.zeros_like(X)
        v_total = np.zeros_like(Y)

        for comp in self.components:
            u, v = comp.velocity_field(X, Y)
            u_total += u
            v_total += v

        return u_total, v_total
    
    def stream_function(self, X, Y):
        psi_total = np.zeros_like(X)

        for comp in self.components:
            psi_total += comp.stream_function(X, Y)

        return psi_total
    
    def pressure_field(self, speed, p0 = 101325.0, rho = 1.225):
        u_inf, v_inf = 0.0, 0.0

        for comp in self.components:
            if isinstance (comp, UniformFlow):
                u_inf += comp.strength * np.cos(comp.alpha)
                v_inf += comp.strength * np.sin(comp.alpha)

        v0_inf = np.sqrt(u_inf**2 + v_inf**2)
        pressure = p0 + 0.5 * rho * (v0_inf**2 - speed**2)

        return pressure
    
    def plot(self, xlim=(-5, 5), ylim=(-5, 5), resolution=200):
        x = np.linspace(xlim[0], xlim[1], resolution)
        y = np.linspace(ylim[0], ylim[1], resolution)
        X, Y = np.meshgrid(x, y)
        
        u, v = self.velocity_field(X, Y)
        psi = self.stream_function(X, Y)
        speed = np.sqrt(u**2 + v**2)
        pressure = self.pressure_field(speed)
        
        plt.figure(figsize=(14, 10))

        #speed_plot = plt.pcolormesh(
        #    X, Y, speed,
        #    cmap='jet',
        #    shading='auto',
        #    vmin=0,
        #    vmax=10,
        #    #vmax=speed.max()
        #)
        #plt.colorbar(speed_plot, label='Speed', shrink=0.8)

        pressure_plot = plt.pcolormesh(
            X, Y, pressure,
            cmap='jet',
            shading='auto',
            vmin=90000,
            vmax=pressure.max()
        )
        plt.colorbar(pressure_plot, label='Pressure', shrink=0.8)
        
        plt.contour(
            X, Y, psi,
            levels=30,
            colors='black',
            linewidths=0.8,
            linestyles='solid'
        )
        
        plt.title('Flow Visualization')
        plt.xlabel('X')
        plt.ylabel('Y')
        plt.gca().set_aspect('equal')
        plt.xlim(xlim)
        plt.ylim(ylim)
        plt.grid(True, linestyle=':', alpha=0.5)
        plt.tight_layout()
        plt.show()

flow = FlowModel()
    
flow.add_component(UniformFlow(strength=100.0, alpha=np.radians(0))) 
# flow.add_component(SourceSink(strength=25.0, dx = 0.0, dy = 0.0))  
# flow.add_component(SourceSink(strength=5.0, dx = 3.0, dy = 0.0))   
flow.add_component(Vortex(strength=-150.0))                  
# flow.add_component(Doublet(strength=7.0))                 
    
flow.plot(xlim=(-5, 5), ylim=(-5, 5), resolution=200)
