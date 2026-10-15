import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier 
#Importa un albero decisionale per problemi di classificazione. per distinguere per segnali buoni o no
from sklearn.metrics import accuracy_score

# =========================
# 1. DATI
# =========================

# Ogni riga rappresenta un'onda
# [ampiezza, durata, rumore]

X = np.array([
	[10, 100, 1],
	[12, 110, 1],
	[11, 105, 2],
	[13, 115, 1],
	[9,  95,  2],

	[50, 300, 10],
	[55, 320, 12],
	[48, 290, 11],
	[60, 350, 15],
	[52, 310, 13]
])

# Categoria associata a ogni onda
# 0 = normale
# 1 = anomala

y = np.array([
	0, 0, 0, 0, 0,
	1, 1, 1, 1, 1
])


# =========================
# 2. DIVIDIAMO I DATI
# =========================


# Perform train-test split
# test_size=0.2 means 20% of the data will be used for testing
# random_state ensures reproducibility --> È semplicemente un numero usato per inizializzare il generatore casuale.
X_train, X_test, y_train, y_test = train_test_split(
	X,
	y,
	test_size=0.3,
	random_state=42
)


# =========================
# 3. CREIAMO IL MODELLO
# =========================

model = DecisionTreeClassifier()

# =========================
# 4. ADDESTRAMENTO
# =========================

model.fit(X_train, y_train)


# =========================
# 5. FACCIAMO DELLE PREVISIONI
# =========================

y_pred = model.predict(X_test)


# =========================
# 6. VALUTIAMO IL MODELLO
# =========================

accuracy = accuracy_score(y_test, y_pred)

print("Accuratezza:", accuracy)


# =========================
# 7. NUOVO DATO
# =========================

nuova_onda = np.array([
	[45, 280, 9]
])

risultato = model.predict(nuova_onda)

print("Classe:", risultato[0])

if risultato[0] == 0:
	print("Onda normale")
else:
	print("Onda anomala")