import math
import numpy as np
import matplotlib.pyplot as plt
import scipy.optimize as opt
from scipy.interpolate import make_interp_spline
from scipy.stats import norm
import matplotlib.mlab as mlab
from sklearn.metrics import r2_score

#function
def gauss(x, A, mu, sigma):
    esponente = ((x-mu)**2) / (2*sigma*sigma)
    norm = A/(np.sqrt(2*np.pi*sigma*sigma))
    return norm*np.exp(-esponente)

#test del chi quadro che torna il chi quadro non ridotto
def test_chi_square(obs, exp, err_exp):
    sum=0
    for i in range(0, len(obs),1):
        sum=((obs[i]-exp[i])/err_exp[i])**2+sum

    return sum


#loading data
x, y = np.loadtxt("lutezio_fit.txt", usecols=(0,1), unpack=True)

#masking data for different fitting functions
#88 kev peak
sx, dx = 60, 150
mask = (x > sx) & (x < dx)
x_fit_1 = (x[mask])
y_fit_1 = y[mask]
err_y_fit1=np.sqrt(y_fit_1)

#88+202 Kev
sx, dx = 370, 490
mask = (x > sx) & (x < dx)
x_fit_2 = (x[mask])
y_fit_2 = y[mask]
err_y_fit2=np.sqrt(y_fit_2)

#88+202+307
sx, dx = 780, 1000
mask = (x > sx) & (x < dx)
x_fit_3 = (x[mask])
y_fit_3 = y[mask]
err_y_fit3=np.sqrt(y_fit_3)

#88+202
sx, dx = 550, 700
mask = (x > sx) & (x < dx)
x_fit_4 = (x[mask])
y_fit_4 = y[mask]
err_y_fit4=np.sqrt(y_fit_4)

#fitting fuction with gauss
#88 kex
p_0 =10000, 150, 50
params_1, cov_1 = opt.curve_fit(gauss, x_fit_1, y_fit_1, p0=p_0, sigma=err_y_fit1)
print('Parametri:', params_1)
#printing dev std of params.
dev_std_1= np.sqrt(np.diag(cov_1))
print('Errori parametri:',dev_std_1)
#chi-square_test
y_opt_1=gauss(x_fit_1, *params_1)
err_exp=np.sqrt(y_opt_1)

chi=test_chi_square(y_fit_1, y_opt_1, err_y_fit1)
print(chi)
n_dof=len(y_fit_1)-len(params_1)
print(n_dof)
print('Reduced chi-square: ', chi/n_dof)

#88+202 kev
p_0 =10000, 460, 100
params_2, cov_2 = opt.curve_fit(gauss, x_fit_2, y_fit_2, p0=p_0, sigma=err_y_fit2)
'''print('Parametri:', params_2)
#printing dev std of params.
dev_std_2= np.sqrt(np.diag(cov_2))
print('Errori parametri:',dev_std_2)
#chi-square_test
y_opt_2=gauss(x_fit_2, *params_2)
err_exp_2=np.sqrt(y_opt_2)

chi=test_chi_square(y_fit_2, y_opt_2, err_exp_2)
n_dof=len(y_fit_2)-len(params_2)
print('Reduced chi-square: ', chi/n_dof)'''

#88+202+307 Kev
p_0 =10000, 960, 250
params_3, cov_3 = opt.curve_fit(gauss, x_fit_3, y_fit_3, p0=p_0, sigma=err_y_fit3)
'''print('Parametri:', params_3)
#printing dev std of params.
dev_std_3= np.sqrt(np.diag(cov_3))
print('Errori parametri:',dev_std_3)
#chi-square_test
y_opt_3=gauss(x_fit_3, *params_3)
err_exp_3=np.sqrt(y_opt_3)

chi=test_chi_square(y_fit_3, y_opt_3, err_exp_3)
n_dof=len(y_fit_3)-len(params_3)-1
print('Reduced chi-square: ', chi/n_dof)'''


#88+307 Kev
p_0 =10000, 600, 50
params_4, cov_4 = opt.curve_fit(gauss, x_fit_4, y_fit_4, p0=p_0, sigma=err_y_fit4)
'''print('Parametri:', params_4)
#printing dev std of params.
dev_std_4= np.sqrt(np.diag(cov_4))
print('Errori parametri:',dev_std_4)
#chi-square_test
y_opt_4=gauss(x_fit_4, *params_4)
err_exp_4=np.sqrt(y_opt_4)

chi=test_chi_square(y_fit_4, y_opt_4, err_exp_4)
n_dof=len(y_fit_4)-len(params_4)-1
print('Reduced chi-square: ', chi/n_dof)
'''

#figure plot
f=plt.figure(num=1)
plt.plot(x, y, label = 'Intrinsic activity',color = 'c', marker=',',linewidth=0.5)
plt.title('Intrinsic activity')#setting title for graph
plt.xlabel('Channels, Ch')#settiting label for axis
plt.ylabel('Counts')

#masking data for plotting
#88Kev
sx, dx = 40, 280
mask = (x > sx) & (x < dx)
x_plot_1 = (x[mask])

#88+202kev
sx, dx = 230, 760
mask = (x > sx) & (x < dx)
x_plot_2 = (x[mask])

#88+202+307kev
sx, dx = 350, 1750
mask = (x > sx) & (x < dx)
x_plot_3 = (x[mask])

#88+307 keV
sx, dx = 50, 1200
mask = (x > sx) & (x < dx)
x_plot_4 = (x[mask])

#plotting the fitting function
plt.plot(x_plot_1, gauss(x_plot_1, *params_1), label= 'Fit_88Kev', color='red')
plt.plot(x_plot_2, gauss(x_plot_2,*params_2), label='Fit_88+202Kev', color='Green')
plt.plot(x_plot_4, gauss(x_plot_4,*params_4), label='Fit_88+307Kev', color='y')
plt.plot(x_plot_3, gauss(x_plot_3,*params_3), label='Fit_88+202+307Kev', color='m')

#linear fit between peaks and energy to find calibration coefficient
#plot in energy: calibration coefficient: Peak= 1.612 energy (+/- 0.030)
g=plt.figure(num=2)
for i in range (0, len(x), +1):
    x[i] = x[i]/1.612
plt.plot(x, y, label = 'Intrinsic activity in Energy',color = 'c', marker=',',linewidth=0.5)
plt.title('Intrinsic activity, Energy')#setting title for graph
plt.xlabel('Energy, keV')#settiting label for axis
plt.ylabel('Counts')


plt.legend()
plt.show()