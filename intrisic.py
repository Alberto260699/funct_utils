import numpy as np
import matplotlib.pyplot as plt
import scipy.optimize as opt
from scipy.interpolate import make_interp_spline
from sklearn.metrics import r2_score
import pandas as pd


def retta (x, m):
    return m*x

#test del chi quadro che torna il chi quadro non ridotto
def test_chi_square(obs, exp, err):
    sum=0
    for i in range(0, len(obs),1):
        sum+=((obs[i]-exp[i])/err[i])**2
    return sum


# load data
x, y , y_err = np.loadtxt("", skiprows=2, usecols=(0,1,2), unpack=True)

file = 'Mio_fit.txt'
df = pd.read_table(file,sep='\s+',skiprows=2, names=['Index','Particle','Energy','Occupation','FermiL','T'])
index=df.iloc[:,0]

#fit
p_0 = 1.5
params, cov = opt.curve_fit(retta, x, y, p0=p_0, sigma=y_err)
print (params)
print (cov)
perr = np.sqrt(np.diag(cov))
print(perr)

#chi-square
chi=test_chi_square(y, retta(x, *params), y_err)
n_dof=len(y)-len(params)
print('Reduced chi-square: ', chi/n_dof)

plt.figure()
plt.errorbar(x, y, yerr=y_err, fmt = 'o', color="blue", label="Data")
plt.plot(x, retta(x, *params), color='red', label='Fit')

plt.title('Calibration')#setting title for graph
plt.xlabel('Energy, keV')#settiting label for axis
plt.ylabel('Peak center')
plt.legend()
plt.show()