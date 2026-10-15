import numpy as np
from scipy.optimize import fsolve

# Valori noti
mu =  0.06
sigma2 =  0.0014
n_h =  0.528
n_l = -0.080

# Funzione obiettivo
def equations(vars):
    p, q = vars
    eq1 = (p / (p - q)) * (n_h - n_l) + n_l - mu
    eq2 = (p * q) / ((p + q)**2 * (p + q + 1)) * (n_h - n_l)**2 - sigma2
    return [eq1, eq2]

# Stima iniziale
initial_guess = [2, 2]

# Risoluzione del sistema
solution = fsolve(equations, initial_guess)

p_sol, q_sol = solution
print(f"p = {p_sol:.4f}, q = {q_sol:.4f}")
