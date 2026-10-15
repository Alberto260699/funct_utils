'''
per la compilazione e esecuzione basta scrivere PYTHON NOME_FILE.PY
'''

import numpy as np
import matplotlib.pyplot as plt
import scipy.optimize as opt

#function
def gauss(x, A, mu, sigma):
    exp = - (x-mu)**2 / 2*sigma**2
    norm = A/(np.sqrt(2* np.pi)*sigma)
    return norm*np.exp(exp)


# load data
x, y = np.loadtxt("intrinsic_activity_003_eh_2.dat", usecols=(0,1), unpack=True)
sx, dx = 9500, 11000  #range del fit
mask = (x > sx) & (x < dx)
x_fit = x[mask]
y_fit = y[mask]

#fit
params, cov = opt.curve_fit(gauss, x_fit, y_fit)

#figure plot riga continua, scatter punti, errorbar per avere ancche errori
plt.figure()
plt.plot(x, y, color="blue", label="data")
plt.plot(x_fit, gauss(x_fit, *params), label= "fit" )
plt.legend()
plt.savefig('plot.pdf')
plt.show()
