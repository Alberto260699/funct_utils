import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

# Parametri iniziali
fs = 1000  # Frequenza di campionamento (Hz)
T = 1.0    # Durata del segnale (secondi)
N = int(fs * T)
t = np.linspace(0, T, N, endpoint=False)

# Funzione per generare il segnale
def generate_signal(f1, f2, a1, a2):
    return a1 * np.sin(2 * np.pi * f1 * t) + a2 * np.sin(2 * np.pi * f2 * t)

# Parametri iniziali
f1_0, f2_0 = 50, 120
a1_0, a2_0 = 0.7, 0.3
signal = generate_signal(f1_0, f2_0, a1_0, a2_0)

# Setup figura
fig, axs = plt.subplots(3, 1, figsize=(10, 8))
plt.subplots_adjust(bottom=0.35)

# Plot iniziali
l_time, = axs[0].plot(t, signal)
axs[0].set_title("Segnale nel dominio del tempo")
axs[0].set_xlabel("Tempo [s]")
axs[0].set_ylabel("Ampiezza")

# FFT iniziale
fft_vals = np.fft.fft(signal)
freqs = np.fft.fftfreq(N, 1/fs)
idx = freqs >= 0
freqs_pos = freqs[idx]
fft_magnitude = np.abs(fft_vals[idx])
power_spectrum = fft_magnitude**2

l_fft, = axs[1].plot(freqs_pos, fft_magnitude)
axs[1].set_title("Modulo della FFT")
axs[1].set_xlabel("Frequenza [Hz]")
axs[1].set_ylabel("Ampiezza |FFT|")

l_power, = axs[2].plot(freqs_pos, power_spectrum)
axs[2].set_title("Spettro di potenza")
axs[2].set_xlabel("Frequenza [Hz]")
axs[2].set_ylabel("Potenza $|FFT|^2$")

# Slider setup
axcolor = 'lightgoldenrodyellow'
ax_f1 = plt.axes([0.15, 0.25, 0.65, 0.03], facecolor=axcolor)
ax_f2 = plt.axes([0.15, 0.20, 0.65, 0.03], facecolor=axcolor)
ax_a1 = plt.axes([0.15, 0.15, 0.65, 0.03], facecolor=axcolor)
ax_a2 = plt.axes([0.15, 0.10, 0.65, 0.03], facecolor=axcolor)

s_f1 = Slider(ax_f1, 'Freq 1 [Hz]', 1, 500, valinit=f1_0)
s_f2 = Slider(ax_f2, 'Freq 2 [Hz]', 1, 500, valinit=f2_0)
s_a1 = Slider(ax_a1, 'Amp 1', 0.0, 10.0, valinit=a1_0)
s_a2 = Slider(ax_a2, 'Amp 2', 0.0, 10.0, valinit=a2_0)

# Funzione di aggiornamento
def update(val):
    f1 = s_f1.val
    f2 = s_f2.val
    a1 = s_a1.val
    a2 = s_a2.val
    new_signal = generate_signal(f1, f2, a1, a2)
    l_time.set_ydata(new_signal)
    
    fft_vals = np.fft.fft(new_signal)
    fft_magnitude = np.abs(fft_vals[idx])
    power_spectrum = fft_magnitude**2
    
    l_fft.set_ydata(fft_magnitude)
    l_power.set_ydata(power_spectrum)
    
    fig.canvas.draw_idle()

# Collega gli slider alla funzione di aggiornamento
s_f1.on_changed(update)
s_f2.on_changed(update)
s_a1.on_changed(update)
s_a2.on_changed(update)

plt.show()
