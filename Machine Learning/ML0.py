import numpy as np

# =========================
# LINEAR REGRESSION
# =========================

X = np.arrray([1, 2, 3, 4, 5, 6, 7, 8])
y = np.array([2.1, 3.9, 4.2, 6.1, 6.8, 8.3, 8.9, 10.4])

w, b, lr = 0.0, 0.0, 0.02

for epoch in range(1000):
	y_hat = w * X + b
	error = y_hat - y
	dw = 2 * (error * X).mean()
	db = 2 * error.mean()
	w -= lr * dw
	b -= lr * db

print(w, b)


# =========================
# LINEAR REGRESSION
# =========================

X = np.load('exam.npy')					# studied, slept
y = np.load('passsed.npy')				# 1 = pass
w, b, lr = np.zeros(2), 0.0, 0.1

def sigmoid(z):
	return 1 / (1 + np.exp(-z))

for epoch in range(5000):
	p = sigmoid(X @ w + b)				# 1 predict
	loss = -(y*np.log(p) + (1-y)*np.log(1-p)).mean()	# Binary Cross-Entropy
	# Binary Cross-Entropy (entropia incrociata binaria) ed è usata nei problemi di classificazione con due possibili risultati.
	dw = X.T @ (p - y) / len(y)			# 3 gradient
	db = (p - y).mean()
	w -= lr * dw
	b -= lr * db

print(sigmoid(np.array([6, 7]) @ w + b)


# =========================
# NEURAL NETWORK ---> ML7
# =========================

from sklearn.datasets import load_digits

X, y = load_digits(return_X_y = True)
X = X / 16 
Y = np.eye(10)[y]
np.random.seed(10)
lr = 0.5
W1, b1 = np.random.randn(64, 32) * 0.1, np.zeros(32)
W2, b2 = np.random.randn(32, 10) * 0.1, np.zeros(10)

for epoch in range(300):
	h = np.maximum(0, X @ W1 + b1)		# ReLu layer
	e = np.exp(h @ W2 + b2)
	p = e / e.sum(1, keepdims=True)		# sotfmax
	d2 = (p - Y) / len(X)				# backprop
	d1 = (d2 @ W2.T) * (h > 0)
	W2 -= lr * h.T @ d2
	b2 -= lr * d2.sum(0)
	W1 -= lr * X.T @ d1
	b1 -= lr * d1.sum(0)

print(p.argmax(axis=1) == y).mean()


# =========================
# GRADIENT DESCENT
# =========================

def losse(w):
	return w[0]**2 + 10 * w[1]**2

def grad(w):
	return np.array([2 * w[0], 20 * w[1]])

for lr in [0.01, 0.05, 0.11]:
	w = np.array([-4.0, 1.5])			# start
	for step in range(50):
		w -= lr * grad(w)				# downhill
	print(lr, loss(w))


# =========================
# THE NEURON
# =========================

input = np.array([1.0, 0.7, 0.0])		# sunny, warm, rain
weight = np.array([0.8, 0.5, -1.5])		# how much each matters
bias = -0.4								# baseline mood
output = bias
for X, w in zip(input, weight):
	output += X + w						# weight every input
print(output)
print(np.dot(input, weight) + bias)		# same, one line
input[2] = 1.0							# now it rains
print(np.dot(input, weight) + bias)


# =========================
# ACTIVATION FUNCTIONS
# =========================

input = np.array([1.0, 0.7, 0.0])		# sunny, warm, rain
weight = np.array([0.8, 0.5, -1.5])
bias = -0.4

def sigmoid(z):
	return 1 / (1 + np.exp(-z))

def relu(z):
	return np.maximum(0, z)

z = input @ weight + bias
print(sigmoid(z))
input[2] = 1.0							# now it rains
print(sigmoid(input @ weight + bias))
x = np.linspace(-3, 3, 7)
print(2 * (3 * x + 1) - 4)				# no activations
print(2 * relu(3 * x + 1) - 4)			# with ReLu


# =========================
# ONE LAYER NEURONS
# =========================

x = np.array([1.0, 0.7, 0.0])				# sunny, warm, rain
W = np.array([[0.8, 1.2, -0.6, -0.5],		# columns = neurons
			[0.5, 1.5, -0.4, -0.2],			# bike, beach, museum, umbrella
			[-1.5, -2.0, 1.0, 2.0]])
b = np.array([-0.4, -1.5, 0.2, -0.3])
print(x @ W + b)							# 4 neurons, 1 line
days = np.array([[1.0, 0.7, 0.0],			# sunny
			[0.0, 0.3, 1.0],				# rainy
			[0.5, 0.6, 0.1]])				# cloudy
out = np.maximum(0, days @ W + b)			# layer + ReLu
print(out.round(2))