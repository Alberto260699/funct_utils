import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from sklearn.model_selection import train_test_split
from torch.utils.data import DataLoader, TensorDataset

# 1. Generazione dei dati (stesso dataset dell'esempio precedente)
np.random.seed(42)
n_samples = 1000
n_timesteps = 100
time = np.linspace(0, 10, n_timesteps)

X, y = [], []
for _ in range(n_samples):
	if np.random.rand() > 0.5:
		signal = np.sin(1 * time) + np.random.normal(0, 0.2, n_timesteps)
		label = 0
	else:
		signal = np.sin(4 * time) + np.random.normal(0, 0.2, n_timesteps)
		label = 1
	X.append(signal)
	y.append(label)

X = np.array(X)
y = np.array(y)

# Divisione in Train e Test
X_train, X_test, y_train, y_test = train_test_split(
	X, y, test_size=0.2, random_state=42
)

# ATTENZIONE: PyTorch vuole lo shape (batch, canali, tempo) -> (N, 1, 100)
X_train = np.expand_dims(X_train, axis=1)
X_test = np.expand_dims(X_test, axis=1)

# Conversione in Tensori PyTorch
X_train_t = torch.tensor(X_train, dtype=torch.float32)
y_train_t = torch.tensor(y_train, dtype=torch.float32).unsqueeze(1)
X_test_t = torch.tensor(X_test, dtype=torch.float32)
y_test_t = torch.tensor(y_test, dtype=torch.float32).unsqueeze(1)

# Creazione dei DataLoader per gestire i mini-batch
train_dataset = TensorDataset(X_train_t, y_train_t)
train_loader = DataLoader(train_dataset, batch_size=32, shuffle=True)


# 2. Definizione dell'Architettura della Rete
class WaveCNN(nn.Module):

	def __init__(self):
		super(WaveCNN, self).__init__()
		# Input: (batch, 1, 100)
		self.conv1 = nn.Conv1d(
			in_channels=1, out_channels=32, kernel_size=3, padding=1
		)
		self.pool = nn.MaxPool1d(kernel_size=2) # Dimezza la lunghezza temporale
		self.conv2 = nn.Conv1d(
			in_channels=32, out_channels=64, kernel_size=3, padding=1
		)
		
		# Dopo due MaxPool da 2, la lunghezza dell'onda passa da 100 a 50, poi a 25
		# 64 canali * 25 elementi temporali = 1600
		self.fc1 = nn.Linear(64 * 25, 64)
		self.dropout = nn.Dropout(0.3)
		self.fc2 = nn.Linear(64, 1)
		self.relu = nn.ReLU()
		self.sigmoid = nn.Sigmoid()

	def forward(self, x):
		x = self.pool(self.relu(self.conv1(x)))
		x = self.pool(self.relu(self.conv2(x)))
		x = x.view(x.size(0), -1) # Appiattimento (Flatten)
		x = self.relu(self.fc1(x))
		x = self.dropout(x)
		x = self.sigmoid(self.fc2(x))
		return x


# Inizializzazione modello, loss e ottimizzatore
model = WaveCNN()
criterion = nn.BCELoss() # Binary Cross Entropy per classificazione binaria
optimizer = optim.Adam(model.parameters(), lr=0.001)

# 3. Ciclo di Addestramento (Training Loop)
epochs = 15
model.train()

for epoch in range(epochs):
	running_loss = 0.0
	for batch_X, batch_y in train_loader:
		optimizer.zero_grad() # Resetta i gradienti del turno precedente
		outputs = model(batch_X) # Passaggio in avanti (Forward pass)
		loss = criterion(outputs, batch_y) # Calcolo dell'errore
		loss.backward() # Passaggio all'indietro (Backpropagation)
		optimizer.step() # Aggiornamento dei pesi
		running_loss += loss.item() * batch_X.size(0)

	epoch_loss = running_loss / len(train_loader.dataset)
	print(f"Epoca {epoch+1}/{epochs} - Loss: {epoch_loss:.4f}")

# 4. Valutazione del Modello
model.eval()
with torch.no_grad(): # Disattiva il calcolo dei gradienti per risparmiare memoria
	predictions = model(X_test_t)
	# Se la probabilità è >= 0.5 la classe è 1, altrimenti 0
	predicted_classes = (predictions >= 0.5).float()
	accuracy = (predicted_classes == y_test_t).float().mean()

print(f"\nAccuratezza del modello PyTorch sul Test Set: {accuracy.item():.4f}")