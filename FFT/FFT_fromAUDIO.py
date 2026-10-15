import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile

# 1. Carica file audio WAV
fs, data = wavfile.read("nome_file.wav")  # Sostituisci col tuo file
print(f"Frequenza di campionamento: {fs} Hz")

# 2. Se stereo, prendi un solo canale
if data.ndim > 1:
    data = data[:, 0]

# 3. Normalizza (opzionale)
data = data / np.max(np.abs(data))

# 4. Vettore temporale
N = len(data)
t = np.arange(N) / fs

# 5. FFT e spettro di potenza
fft_vals = np.fft.fft(data)
freqs = np.fft.fftfreq(N, 1/fs)
idx = freqs >= 0
freqs_pos = freqs[idx]
fft_magnitude = np.abs(fft_vals[idx])
power_spectrum = fft_magnitude**2

# 6. Plot
plt.figure(figsize=(12, 8))

plt.subplot(3, 1, 1)
plt.plot(t, data)
plt.title("Segnale audio nel dominio del tempo")
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
