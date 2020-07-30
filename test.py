import numpy as np
from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation
plt.style.use('seaborn-pastel')

fig = plt.figure()
ax1 = fig.add_subplot(2, 1, 1, aspect='equal')
ax2 = fig.add_subplot(2, 1, 2, aspect='equal')
ax1.set_xlim(0, 1)
ax2.set_xlim(0, 1)
ax1.set_ylim(0, 1)
ax2.set_ylim(0, 1)
line, = ax2.plot([], [], lw=3) 

def init():
    line.set_data([], [])
    return (line,)

def animate(i):
    x = np.linspace(0, 4, 1000)
    y = np.sin(2 * np.pi * (x - 0.01 * i))
    line.set_data(x, y)
    return (line,)

anim = FuncAnimation(fig, animate, init_func=init,
                               frames=200, interval=20, blit=True)


anim.save('sine_wave.gif', writer='imagemagick')
