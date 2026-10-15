import numpy as np
import matplotlib.pyplot as plt

# Crea un esempio di segnale 2D (può essere sostituito con un'immagine reale)
def crea_segnale_2d(dim=(256, 256)):
    x = np.linspace(0, 4 * np.pi, dim[0])
    y = np.linspace(0, 4 * np.pi, dim[1])
    X, Y = np.meshgrid(x, y)
    segnale = np.sin(X) + np.cos(Y)
    return segnale

# Calcolo della trasformata di Fourier 2D
def calcola_fft2(segnale):
    fft2 = np.fft.fft2(segnale)
    fft2_shifted = np.fft.fftshift(fft2)  # Centra lo zero in mezzo
    return fft2_shifted

# Calcolo dello spettro di potenza
def calcola_spettro_potenza(fft2_shifted):
    potenza = np.abs(fft2_shifted) ** 2
    return potenza

# Visualizzazione
def mostra_risultati(segnale, spettro_potenza):
    plt.figure(figsize=(12, 5))

    plt.subplot(1, 2, 1)
    plt.title("Segnale originale")
    plt.imshow(segnale, cmap='gray')
    plt.colorbar()

    plt.subplot(1, 2, 2)
    plt.title("Spettro di potenza (log scale)")
    plt.imshow(np.log1p(spettro_potenza), cmap='inferno')  # log1p per visualizzare meglio
    plt.colorbar()

    plt.tight_layout()
    plt.show()

# Esecuzione
if __name__ == "__main__":
    segnale = crea_segnale_2d()
    fft2_shifted = calcola_fft2(segnale)
    spettro_potenza = calcola_spettro_potenza(fft2_shifted)
    mostra_risultati(segnale, spettro_potenza)
