import numpy as np
from sklearn.ensemble import RandomForestClassifier
#Importa una Random Forest, cioè un insieme di molti alberi decisionali. Ogni albero dà la propria classificazione e la Random Forest combina i risultati.
from sklearn.metrics import accuracy_score, r2_score
from sklearn.model_selection import train_test_split

# 1. Creazione di un dataset sintetico di onde
np.random.seed(42)
n_samples = 200
time = np.linspace(0, 10, 100)

X = []
y = []

for _ in range(n_samples):
	# Classe 0: onda a bassa frequenza
	if np.random.rand() > 0.5:
		signal = np.sin(1 * time) + np.random.normal(0, 0.1, len(time))
		label = 0
	# Classe 1: onda ad alta frequenza
	else:
		signal = np.sin(5 * time) + np.random.normal(0, 0.1, len(time))
		label = 1

	# 2. Estrazione delle feature (es. media, deviazione standard, energia)
	feat_mean = np.mean(signal)
	feat_std = np.std(signal)
	feat_max = np.max(signal)
	feat_min = np.min(signal)

	X.append([feat_mean, feat_std, feat_max, feat_min])
	y.append(label)

X = np.array(X)
y = np.array(y)

# 3. Divisione in Training e Test set
X_train, X_test, y_train, y_test = train_test_split(
	X, y, test_size=0.2, random_state=42
)

# 4. Addestramento del modello
model = RandomForestClassifier(random_state=42)
model.fit(X_train, y_train)

# 5. Valutazione
y_pred = model.predict(X_test)
print("Accuratezza del modello:", accuracy_score(y_test, y_pred))
print('R^2: ', r2_score(y_test, y_pred))