#library
#%matplotlib qt5#da usare solo su jupyter
import numpy as np#importi tutta la libreria
import matplotlib.pyplot as plt
import pandas as pd
import scipy.optimize as opt
import scipy.signal as sig#filtra il segnale
from sklearn.metrics import r2_score#importi solo la funzione dalla libreria

#function gauss
def gauss(x,A,mu,sigma):
    exp = -(x-mu)**2/(2*sigma**2)
    norm = A/(np.sqrt(2*np.pi)*sigma)
    return norm*np.exp(exp)
	
#load data
file='Spettro_plasma.txt'
dati=pd.read_table(file, sep='\s+', skiprows=0, names=['Channel (Ch)','Counts (#)'])
x=dati.iloc[:,0]
y=dati.iloc[:,1]
yhat=sig.savgol_filter(y, 41, 3)#filtering data
mask=(x>8000)&(x<10000)
x_fit = x[mask]
y_fit = yhat[mask]
y_err=np.sqrt(y_fit)

#fit
p_0=87500, 8900, 400
popt, pcov=opt.curve_fit(gauss, x_fit, y_fit, p_0, y_err)
print(popt)
print(pcov)
perr=np.sqrt(np.diag(pcov))
print(perr)
yopt=gauss(x_fit, *popt)
print('R^2: ', r2_score(yopt, y_fit))

#plot
plt.figure()
plt.plot(x_fit, y_fit, color='blue', label='Data')
plt.plot(x_fit, gauss(x_fit, *popt), color='red', label='Fit1')
plt.legend()
plt.xlabel('Channel(Ch)')
plt.ylabel('Counts')
plt.savefig('Plasma_spectrum.png')
plt.show()