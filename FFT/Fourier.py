import numpy as np
import matplotlib.pyplot as plt

# =========================
# 1. Creazione del segnale
# =========================
fs = 1000  # frequenza di campionamento (Hz)
t = np.arange(0, 1, 1/fs)

f_signal = 50  # frequenza del segnale
x = np.sin(2 * np.pi * f_signal * t)

# =========================
# 2. FFT senza finestra
# =========================
X = np.fft.fft(x)
freqs = np.fft.fftfreq(len(x), 1/fs)

# =========================
# 3. FFT con finestra Hamming
# =========================
window = np.hamming(len(x))
x_win = x * window

X_win = np.fft.fft(x_win)

# =========================
# 4. Solo frequenze positive
# =========================
mask = freqs >= 0

freqs_pos = freqs[mask]
X_pos = np.abs(X[mask])
X_win_pos = np.abs(X_win[mask])

# =========================
# 5. Plot senza finestra
# =========================
plt.figure()
plt.plot(freqs_pos, X_pos)
plt.title("FFT senza finestra")
plt.xlabel("Frequenza (Hz)")
plt.ylabel("Ampiezza")
plt.grid()

# =========================
# 6. Plot con Hamming
# =========================
plt.figure()
plt.plot(freqs_pos, X_win_pos)
plt.title("FFT con finestra di Hamming")
plt.xlabel("Frequenza (Hz)")
plt.ylabel("Ampiezza")
plt.grid()

plt.show()


'''

Finestra	Leakage			Precisione frequenza	Uso tipico
Nessuna		❌ alto			✔ alta (teorica)		quasi mai
Hamming		✔ medio-basso	✔ buona	standard
Hann		✔ basso			❌ media					analisi generale
Blackman	✅ molto basso	❌ più bassa				segnali rumorosi

'''

import numpy as np
import matplotlib.pyplot as plt

# =========================
# 1. Creazione segnale
# =========================
fs = 1000  # Hz
t = np.arange(0, 1, 1/fs)

f_signal = 53.7  # frequenza NON multipla → leakage
x = np.sin(2 * np.pi * f_signal * t)

# =========================
# 2. Definizione finestre
# =========================
windows = {
    "Nessuna finestra": np.ones(len(x)),
    "Hamming": np.hamming(len(x)),
    "Hann": np.hanning(len(x)),
    "Blackman": np.blackman(len(x)),
}

# =========================
# 3. FFT e plotting
# =========================
freqs = np.fft.fftfreq(len(x), 1/fs)
mask = freqs >= 0
freqs_pos = freqs[mask]

for name, w in windows.items():
    xw = x * w
    X = np.fft.fft(xw)
    
    X_pos = np.abs(X[mask]) / len(x)

    plt.figure()
    plt.plot(freqs_pos, X_pos)
    plt.title(f"FFT con finestra: {name}")
    plt.xlabel("Frequenza (Hz)")
    plt.ylabel("Ampiezza")
    plt.grid()

plt.show()
'''
#se vuo un confronte rapido e averli tutti nella stessa finestra
plt.figure()

for name, w in windows.items():
    xw = x * w
    X = np.fft.fft(xw)
    X_pos = np.abs(X[mask]) / len(x)

    plt.plot(freqs_pos, X_pos, label=name)

plt.title("Confronto finestre")
plt.xlabel("Frequenza (Hz)")
plt.ylabel("Ampiezza")
plt.legend()
plt.grid()

plt.show()
'''