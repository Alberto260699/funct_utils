import numpy as np
import tensorflow as tf
from sklearn.model_selection import train_test_split
from tensorflow.keras import layers, models

# 1. Generazione di dati sintetici (onde grezze)
np.random.seed(42)
n_samples = 1000
n_timesteps = 100 # Lunghezza di ogni singola onda
time = np.linspace(0, 10, n_timesteps)

X = []
y = []

for _ in range(n_samples):
	if np.random.rand() > 0.5:
		# Classe 0: Onda a bassa frequenza + rumore
		signal = np.sin(1 * time) + np.random.normal(0, 0.2, n_timesteps)
		label = 0
	else:
		# Classe 1: Onda ad alta frequenza + rumore
		signal = np.sin(4 * time) + np.random.normal(0, 0.2, n_timesteps)
		label = 1
	X.append(signal)
	y.append(label)

X = np.array(X)
y = np.array(y)

# Per le CNN 1D, i dati devono avere la forma (campioni, passi_temporali, caratteristiche)
# In questo caso abbiamo 1 sola caratteristica (l'ampiezza dell'onda nel tempo)
X = np.expand_dims(X, axis=-1)

# 2. Divisione in Training e Test set
X_train, X_test, y_train, y_test = train_test_split(
	X, y, test_size=0.2, random_state=42
)

# 3. Costruzione della Rete Neurale Convoluzionale (CNN 1D)
model = models.Sequential([
		# Primo blocco convoluzionale per estrarre pattern temporali
		layers.Conv1D(
			filters=32, kernel_size=3, activation="relu", input_shape=(100, 1)
		),
		layers.MaxPooling1D(pool_size=2),
		# Secondo blocco convoluzionale
		layers.Conv1D(filters=64, kernel_size=3, activation="relu"),
		layers.MaxPooling1D(pool_size=2),
		# Appiattimento dei dati per i livelli densi
		layers.Flatten(),
		layers.Dense(64, activation="relu"),
		layers.Dropout(0.3), # Riduce il rischio di overfitting
		# Livello di output (funzione sigmoid per classificazione binaria 0 o 1)
		layers.Dense(1, activation="sigmoid"),
])

# 4. Compilazione del modello
model.compile(
	optimizer="adam", loss="binary_crossentropy", metrics=["accuracy"]
)

# 5. Addestramento della rete
history = model.fit(
	X_train,
	y_train,
	epochs=15,
	batch_size=32,
	validation_data=(X_test, y_test),
	verbose=1,
)

# 6. Valutazione finale
test_loss, test_acc = model.evaluate(X_test, y_test, verbose=0)
print(f"\nAccuratezza della Rete Neurale sul Test Set: {test_acc:.4f}")