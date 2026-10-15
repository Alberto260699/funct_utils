import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

# Funzione per creare un segnale 2D con una frequenza variabile
def crea_segnale_2d(freq=1.0, dim=(256, 256)):
    x = np.linspace(0, 4 * np.pi, dim[0])
    y = np.linspace(0, 4 * np.pi, dim[1])
    X, Y = np.meshgrid(x, y)
    segnale = np.sin(freq * X) + np.cos(freq * Y)
    return segnale

# Funzione per calcolare FFT2 e spettro di potenza
def calcola_fft_spettro(segnale):
    fft2 = np.fft.fft2(segnale)
    fft2_shifted = np.fft.fftshift(fft2)
    spettro_potenza = np.abs(fft2_shifted) ** 2
    return spettro_potenza

# Setup figura e assi
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
plt.subplots_adjust(bottom=0.25)

# Inizializzazione
freq_iniziale = 1.0
segnale = crea_segnale_2d(freq_iniziale)
spettro = calcola_fft_spettro(segnale)

# Immagini iniziali
img1 = ax1.imshow(segnale, cmap='gray')
ax1.set_title("Segnale 2D")

img2 = ax2.imshow(np.log1p(spettro), cmap='inferno')
ax2.set_title("Spettro di potenza (log scale)")

# Slider
ax_slider = plt.axes([0.25, 0.1, 0.5, 0.03])
slider_freq = Slider(ax_slider, 'Frequenza', 0.1, 10.0, valinit=freq_iniziale)

# Funzione aggiorna slider
def aggiorna(val):
    freq = slider_freq.val
    nuovo_segnale = crea_segnale_2d(freq)
    nuovo_spettro = calcola_fft_spettro(nuovo_segnale)

    img1.set_data(nuovo_segnale)
    img2.set_data(np.log1p(nuovo_spettro))

    fig.canvas.draw_idle()

slider_freq.on_changed(aggiorna)

plt.show()
