import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Creazione della figura e degli assi
fig, ax = plt.subplots()
xdata, ydata = [], []
ln, = plt.plot([], [], 'ro')

# Funzione di inizializzazione
def init():
    ax.set_xlim(0, 4 * np.pi)
    ax.set_ylim(-1, 1)
    return ln,

# Funzione di aggiornamento dell'animazione
def update(frame):
    xdata.append(frame)
    ydata.append(np.sin(frame))
    ln.set_data(xdata, ydata)
    return ln,

# Creazione dell'animazione
ani = FuncAnimation(fig, update, frames=np.linspace(0, 4 * np.pi, 240),
                    init_func=init, blit=True)

plt.show()
