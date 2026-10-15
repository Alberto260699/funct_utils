import numpy as np
import matplotlib.pyplot as plt

# Carica dati da CSV
data = np.loadtxt("segnale.csv")  # Una colonna con i valori del segnale

# Parametri noti
fs = 1000  # Frequenza di campionamento in Hz (modifica se necessario)
N = len(data)
t = np.arange(N) / fs

# FFT
fft_vals = np.fft.fft(data)
freqs = np.fft.fftfreq(N, 1/fs)
idx = freqs >= 0
freqs_pos = freqs[idx]
fft_magnitude = np.abs(fft_vals[idx])
power_spectrum = fft_magnitude**2

# Plot
plt.figure(figsize=(12, 8))

plt.subplot(3, 1, 1)
plt.plot(t, data)
plt.title("Segnale CSV nel dominio del tempo")
plt.xlabel("Tempo [s]")
plt.ylabel("Ampiezza")

plt.subplot(3, 1, 2)
plt.stem(freqs_pos, fft_magnitude, basefmt=" ", use_line_collection=True)
plt.title("Modulo FFT")
plt.xlabel("Frequenza [Hz]")
plt.ylabel("Ampiezza")

plt.subplot(3, 1, 3)
plt.plot(freqs_pos, power_spectrum)
plt.title("Spettro di potenza")
plt.xlabel("Frequenza [Hz]")
plt.ylabel("Potenza")

plt.tight_layout()
plt.show()
