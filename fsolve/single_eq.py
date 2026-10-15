import numpy as np
from scipy.optimize import minimize

# Valori noti
mu = 0.06
sigma2 = 0.0014
n_h = 0.528
n_l = -0.080

# Funzione obiettivo: somma dei quadrati degli errori delle due equazioni
def objective(vars):
    p, q = vars
    # Evita divisioni per zero o valori non validi
    if p <= 0 or q <= 0 or p == q:
        return 1e10
    eq1 = (p / (p - q)) * (n_h - n_l) + n_l - mu
    eq2 = (p * q) / ((p + q)**2 * (p + q + 1)) * (n_h - n_l)**2 - sigma2
    return [eq1, eq2]

# Limiti: p > 0, q > 0
bounds = [(1e-6, None), (1e-6, None)]

# Stima iniziale
initial_guess = [10, 30]

# Minimizzazione
res = minimize(objective, initial_guess, bounds=bounds)

# Risultato
if res.success:
    p_opt, q_opt = res.x
    print(f"Soluzione trovata con minimize:")
    print(f"p = {p_opt:.4f}, q = {q_opt:.4f}")
else:
    print("Minimizzazione fallita:", res.message)
