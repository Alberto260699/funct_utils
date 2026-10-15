from sympy import Symbol, cos, sin, exp, diff, integrate, limit, solve, oo, pi

# Define symbols
x = Symbol('x')
y = Symbol('y')

# Differentiation
derivative = diff(sin(x) * exp(x), x)

# Integration
indefinite_integral = integrate(exp(x) * sin(x) + exp(x) * cos(x), x)
definite_integral = integrate(sin(x**2), (x, -oo, oo))

# Limit
lim = limit(sin(x)/x, x, 0)

# Solving equations
solutions = solve(x**2 - 2, x)

# Special constants like pi and infinity
p = pi**3
result_with_infinity = oo + 10000

def taylor(f, x_0=0, n=2):
	'''
	Calcola l'espansione di Taylor della funzione f attorno a x_0 fino all'ordine n.
	
	Parametri:
		f : funzione simbolica o stringa (es. 'sin(x)', sp.exp(x))
		x_0 : punto attorno al quale si espande la funzione
		n : ordine dell'espansione

	Ritorna:
		Serie di Taylor semplificata (senza termine O)
	'''
	x = sp.Symbol('x')
	f = sp.sympify(f)  # converte da stringa o espressione a forma simbolica

	taylor_series = f.series(x, x_0, n+1).removeO()
	return taylor_series

# Esempi d’uso
print(taylor('sin(x)', 0, 5))
print(taylor(sp.exp(x), 0, 4))
print(taylor('cos(x)', sp.pi/4, 3))