# =========================
# RETE NEURALE CON NUMPY
# =========================

import numpy as np
from sklearn.datasets import load_digits

# 1. Caricamento dei dati
X, y = load_digits(return_X_y=True)

# Normalizziamo i pixel tra 0 e 1
X = X / 16

# Trasformiamo le etichette in formato one-hot
Y = np.eye(10)[y]

# 2. Inizializzazione dei parametri
np.random.seed(42)
lr = 0.5

W1 = np.random.randn(64, 32) * 0.1
b1 = np.zeros(32)

W2 = np.random.randn(32, 10) * 0.1
b2 = np.zeros(10)

# 3. Addestramento
for epoch in range(300):

	# Livello nascosto: prodotto + bias + ReLU
	z1 = X @ W1 + b1
	h = np.maximum(0, z1)			

	# Livello di output
	z2 = h @ W2 + b2

	# Softmax, con stabilizzazione numerica
	z2 = z2 - z2.max(axis=1, keepdims=True)		# Stabilizza
	e = np.exp(z2)								# Esponenziale
	p = e / e.sum(axis=1, keepdims=True)		# Softmax

	# Backpropagation
	d2 = (p - Y) / len(X)						# dL / dz2
	d1 = (d2 @ W2.T) * (z1 > 0)					# chain rule

	# Aggiornamento dei parametri
	W2 -= lr * (h.T @ d2)
	b2 -= lr * d2.sum(axis=0)

	W1 -= lr * (X.T @ d1)
	b1 -= lr * d1.sum(axis=0)

# 4. Valutazione sul dataset di addestramento
predizioni = p.argmax(axis=1)
accuratezza = (predizioni == y).mean()

print("Accuratezza:", accuratezza)

'''
def forward(X):
	z1 = X @ W1 + b1
	h = np.maximum(0, z1)

	z2 = h @ W2 + b2

	e = np.exp(z2 - z2.max(axis=1, keepdims=True))
	p = e / e.sum(axis=1, keepdims=True)

	return p, h

def loss(p, Y):
	return -np.mean(np.sum(Y * np.log(p * 1e-9), 1))

def backward(X, Y, h, p):
	d2 = (p - Y) / len(X)
	d1 = (d2 @ W2.T) * (h > 0)
	return X.T @ d1, d1.sum(axis=0), h.T @ d2, d2.sum(axis=0)
'''




# post addestramento posso provare con una immmagine di prova


from PIL import Image
import numpy as np

# Apriamo l'immagine
img = Image.open("numero.png")

# La convertiamo in scala di grigi e la ridimensioniamo
img = img.convert("L").resize((8, 8))
# convert("L") converte l'immagine in scala di grigi. resize((8, 8)) la porta a 8 × 8 pixel

# Convertiamo l'immagine in un array NumPy
X_nuovo = np.array(img)

print(X_nuovo)
print(X_nuovo.shape)

X_nuovo = X_nuovo / 255.0 				# sfondo scuro e cifra bianca
X_nuovo = 1.0 - X_nuovo / 255.0			# sfondo chiaro e cifra nera

X_nuovo = X_nuovo.reshape(1, 64)

# Primo livello: 64 input -> 32 neuroni
h = np.maximum(0, X_nuovo @ W1 + b1)

# Secondo livello: 32 neuroni -> 10 classi
z2 = h @ W2 + b2

# Softmax stabile
z2 = z2 - z2.max(axis=1, keepdims=True)
e = np.exp(z2)
p = e / e.sum(axis=1, keepdims=True)

# Cifra con probabilità maggiore
cifra = p.argmax(axis=1)[0]

print("La cifra riconosciuta è:", cifra)
print("Probabilità per ogni cifra:", p[0])