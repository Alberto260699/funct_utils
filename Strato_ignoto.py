#library
#%matplotlib qt5
import math
import numpy as np#importi tutta la libreria
import matplotlib.pyplot as plt
import pandas as pd
import sympy as sp#utile per funzioni di derivazione
import scipy.optimize as opt
import scipy.signal as sig#ripulisce il segnale filtrandolo 
from sklearn.metrics import r2_score#importi solo la funzione dalla libreria

#function
def gauss(x,A,mu,sigma):
    exp=-(x-mu)**2/(2*sigma**2)
    norm=A/(np.sqrt(2*np.pi)*sigma)
    return norm*np.exp(exp)
def diff_gauss(x,A,mu,sigma):
    exp=-(x-mu)**2/(2*sigma**2)
    norm=-A*(2*x-2*mu)/(np.sqrt(2*np.pi)*2*sigma**3)
    return norm*np.exp(exp)
    
#load data
file='Strato_ignoto.txt'
dati=pd.read_table(file, sep='\s+', skiprows=0, names=['Channel(Ch)','Counts(#)'])
x=dati.iloc[:,0]
y=dati.iloc[:,1]
mask=(x>0)&(x<10000)
x_fit=x[mask]
y_fit=y[mask]

#fit
p_0=43750, 4374.28, 1011.71
popt, pcov=opt.curve_fit(gauss, x_fit, y_fit, p_0)
print(popt)
print(pcov)
perr=np.sqrt(np.diag(pcov))
print(perr)
yopt=gauss(x_fit, *popt)
print('R^2: ', r2_score(yopt, y_fit))

#derivate
l=sp.Symbol('lambda')
A=sp.Symbol('A')
mu=sp.Symbol('mu')
sigma=sp.Symbol('sigma')
pi=sp.Symbol('pi')
exp=sp.Symbol('e')
two=sp.Symbol('2')
z=(A/((two*pi)**(1/2)*sigma))*exp**(-(l-mu)**2/(2*sigma**2))
sp.diff(z, l)

#plot
plt.figure()
plt.plot(x_fit, y_fit, color='blue', label='Data')
plt.plot(x_fit, gauss(x_fit, *popt), color='red', label='Fit')
plt.plot(x_fit, diff_gauss(x_fit, *popt), color='green', label='Derivate')
plt.legend()
plt.xlabel('Channel(Ch)')
plt.ylabel('Counts')
plt.savefig('Unknown_layer.png')
plt.show()