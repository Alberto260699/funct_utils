# ==========================================
# 1. IMPORT
# ==========================================

from sklearn.datasets import load_iris			# -> carica il dataset precompilato iris
from sklearn.model_selection import train_test_split

# Classifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import (
	RandomForestClassifier,
	GradientBoostingClassifier,
	AdaBoostClassifier,
	ExtraTreesClassifier
)

from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.naive_bayes import GaussianNB
from sklearn.neural_network import MLPClassifier

# Metriche
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, r2_score


# ==========================================
# 2. CARICHIAMO IL DATASET
# ==========================================

iris = load_iris()

X = iris.data
y = iris.target

print("Forma di X:", X.shape)
print("Forma di y:", y.shape)
print("Classi:", iris.target_names)


# ==========================================
# 3. DIVIDIAMO I DATI
# ==========================================

X_train, X_test, y_train, y_test = train_test_split(
	X,
	y,
	test_size=0.2,
	random_state=42,
	stratify=y
)


# ==========================================
# 4. CREIAMO I MODELLI
# ==========================================

models = {
	
	"Decision Tree":
		DecisionTreeClassifier(random_state=42),
	
	"Random Forest":
		RandomForestClassifier(
			n_estimators=100,
			random_state=42
		),
	
	"KNN":
		KNeighborsClassifier(n_neighbors=5),
	
	"Logistic Regression":
		LogisticRegression(max_iter=1000),
	
	"SVM":
		SVC(),
	
	"Naive Bayes":
		GaussianNB(),
	
	"Gradient Boosting":
		GradientBoostingClassifier(random_state=42),
	
	"AdaBoost":
		AdaBoostClassifier(random_state=42),
	
	"Extra Trees":
		ExtraTreesClassifier(
			n_estimators=100,
			random_state=42
		),
	
	"Neural Network":
		MLPClassifier(
			hidden_layer_sizes=(64, 32),
			max_iter=1000,
			random_state=42
		)
}


# ==========================================
# 5. ALLENIAMO E TESTIAMO I MODELLI
# ==========================================

results = []


for name, model in models.items():
	
	print("\n==============================")
	print(name)
	print("==============================")
	
	# Addestramento
	model.fit(X_train, y_train)
	
	# Predizione
	y_pred = model.predict(X_test)
	
	# Metriche
	accuracy = accuracy_score(y_test, y_pred)
	
	precision = precision_score(
		y_test,
		y_pred,
		average="weighted"
	)
	
	recall = recall_score(
		y_test,
		y_pred,
		average="weighted"
	)
	
	f1 = f1_score(
		y_test,
		y_pred,
		average="weighted"
	)
	
	r2 = r2_score(
		y_test,
		y_pred
	)
	
	print("Accuracy :", accuracy)
	print("Precision:", precision)
	print("Recall   :", recall)
	print("F1-score :", f1)
	print("R2-score :", r2)
	
	results.append(
		(
			name,
			accuracy,
			precision,
			recall,
			f1,
			r2
		)
	)


# ==========================================
# 6. CONFRONTO FINALE
# ==========================================

print("\n\n==============================================")
print("CONFRONTO DEI MODELLI")
print("==============================================")

print(
	f"{'Modello':<25}"
	f"{'Accuracy':<12}"
	f"{'Precision':<12}"
	f"{'Recall':<12}"
	f"{'F1':<12}"
	f"{'R2':<12}"
)

print("-" * 83)


for result in results:
	
	name, accuracy, precision, recall, f1, r2 = result
	
	print(
		f"{name:<25}|"
		f"{accuracy:<12.3f}"
		f"{precision:<12.3f}"
		f"{recall:<12.3f}"
		f"{f1:<12.3f}"
		f"{r2:<12.3f}"
	)


'''
f"{accuracy:<12.3f}|"
	| → inserisce il simbolo
	< → allineato a sinistra
	12 → occupa 12 caratteri
	.3f → mostra 3 cifre decimali
'''