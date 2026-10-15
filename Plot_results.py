import numpy as np
import matplotlib.pyplot as plt

#load data
fl='Results_0.0077P.txt'
pos_probe, V_fl, err_V_fl, T_e, err_T_e, n_e, err_n_e=np.loadtxt(fl, delimiter=', ', skiprows=1, usecols=(3,4,5,6,7,8,9), unpack=True)

#plot data
fig=plt.figure(figsize=(18,5))
ax1=fig.add_subplot(131).scatter(pos_probe, V_fl, color='red')
plt.errorbar(pos_probe, V_fl, err_V_fl)
plt.title('Plot V_fl')
plt.xlabel('Position probe (cm)')
plt.ylabel('V_fl (V)')
plt.grid(linestyle='dashed')

ax2=fig.add_subplot(132).scatter(pos_probe, T_e, color='red')
plt.errorbar(pos_probe, T_e, err_T_e)
plt.title('Plot T_e')
plt.xlabel('Position probe (cm)')
plt.ylabel('T_e (eV)')
plt.grid(linestyle='dashed')

ax3=fig.add_subplot(133).scatter(pos_probe, n_e, color='red')
plt.errorbar(pos_probe, n_e, err_n_e)
plt.title('Plot n_e')
plt.xlabel('Position probe (cm)')
plt.ylabel('n_e (N/cm^3)')
plt.grid(linestyle='dashed')

plt.savefig('Results_0.0077P.png')
plt.show()