# =========================
# RETE NEURALE
# =========================

import numpy as np
import tensorflow as tf
from tensorflow import keras

# =========================
# 1. CREIAMO I DATI
# =========================

X = []
y = []


for i in range(1000):

	x = np.linspace(0, 1000, 200)

	# Picco principale
	signal = 100 * np.exp(
		-((x - 500) ** 2) / (2 * 35 ** 2)
	)

	# Rumore
	noise = np.random.normal(0, 5, len(x))

	signal += noise

	# 50% segnali anomali
	if i >= 500:

		# Aggiungiamo un secondo picco
		signal += 40 * np.exp(
			-((x - 700) ** 2) / (2 * 20 ** 2)
		)

		y.append(1)

	else:
		y.append(0)

	X.append(signal)


X = np.array(X)
y = np.array(y)


# =========================
# 2. CREIAMO LA RETE
# =========================

model = keras.Sequential([

	keras.layers.Input(shape=(200,)),

	keras.layers.Dense(64, activation="relu"),

	keras.layers.Dense(32, activation="relu"),

	keras.layers.Dense(1, activation="sigmoid")
])

'''
LAYER DI OUTPUT
keras.layers.Dense(1, activation="sigmoid") --> se vuoi avere una differenziazione 0/1 (anomala/normale)
keras.layers.Dense(10, activation="softmax") --> se vuoi avere una differenziazione tra più classi
keras.layers.Dense(1, activation="linear") --> nessuna attivazione, se vuoi prevedere il valore di un segnale senza limitarla tra 0 e 1

keras.layers.Dense(3, activation="sigmoid") --> se vuoi analizzare 3 diverse caratteristiche sempre avendo la probabilità compresa 0/1

ATTIVAZIONE DEL NEURONE
keras.layers.Dense(64, activation="tanh") --> come sigmoide ma in intervallo -1/1
keras.layers.Dense(64, activation="elu")
keras.layers.Dense(64, activation="gelu")
keras.layers.Dense(64, activation="selu")
keras.layers.Dense(64, activation="softplus")
keras.layers.Dense(64, activation="leaky_relu")
keras.layers.Dense(64, activation="silu")
keras.layers.Dense(64, activation="prelu")
'''


# =========================
# 3. CONFIGURIAMO LA RETE
# =========================

model.compile(
	optimizer="adam",
	loss="binary_crossentropy",
	metrics=["accuracy"]
)

'''
VARI TIPI DI LOSSES (a seconda del caso)
loss="binary_crossentropy", --> buono per 0/1 <-- loss = -(y*np.log(p) + (1-y)*np.log(1-p)).mean()
loss="mean_absolute_error", --> buono per una regressione lineare <-- loss = (y - y_hat).mean()
loss="mean_squared_error", --> buono per una regressione lineare <-- loss = ((y - y_hat)**2).mean()
loss="categorical_crossentropy", --> buono per il multiclasse <-- loss = -np.log(p)

ALTRO MODO PER RICHIAMARE I COMANDI
loss=keras.losses.MeanAbsoluteError(),
'''


# =========================
# 4. ADDESTRAMENTO
# =========================

model.fit(
	X,
	y,
	epochs=20,
	batch_size=32	#quanti segnali elabori alla volta
	#verbose=1
)

# =========================
# 5. TEST DI UN NUOVO SEGNALE
# =========================

x = np.linspace(0, 1000, 200)

signal = 100 * np.exp(
	-((x - 500) ** 2) / (2 * 35 ** 2)
)

noise = np.random.normal(0, 5, len(x))

signal += noise


# Prepariamo il segnale
signal_input = signal.reshape(1, 200)


# Predizione
prediction = model.predict(signal_input)[0][0]


print("Probabilità di anomalia:", prediction)


if prediction >= 0.5:
	print("SEGNALE ANOMALO")
else:
	print("SEGNALE NORMALE")