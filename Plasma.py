#%matplotlib qt5# da usare solo su jupyter
#library
import numpy as np
import matplotlib.pyplot as plt
import scipy.signal as sig
import scipy.optimize as opt
from sklearn.metrics import r2_score

#functions
def retta(x, m, q):
    return q+m*x

#modello semplificato (B=0)
'''REGIONE DI SATURAZIONE IONICA
def I_isat():
    return 0.6*e*n_e*A_eff*np.sqrt(T_e/m_i)'''

'''REGIONE DI SATURAZIONE ELETTRONICA
def I_esat():
    return -e*n_e*A_eff*np.sqrt(T_e/2*np.pi*m_e)'''

'''REGIONE DI TRANSIZIONE
def I_e():
    return I_esat*np.exp(e*(V-V_pl)/T_e)
def logIe():
    return np.log(I_esat)-e*V_pl/T_e+e*V/T_e #-->q+m*V
#quello che ottieni è un andamento lineare dove m=1/T_e
def I():
    return I_isat()+I_e()
#NB: puoi trovare Ie come --> I-I_isat=I_e'''

'''FIND V PLASMA
def V_pl():
    return V_fl+T_e*log(I_isat/I_esat)
#oppure puoi trovare Vpl come intersezione di 2 rette'''

#FIT 4 PARAMETERS
def I(V, I_isat, a, V_fl, T_e):
    return I_isat*(1-a*(V-V_fl)-np.exp((V-V_fl)/T_e))
#NB: non descrivi quello che viene dopo il potenziale di plasma

#modello NON semplificato (B!=0)
'''AREA EFFICACE DELLA SONDA
def A_eff(A_perp, x_g, r):
    return A_perp(1+(x_g/r))
def x_g(debay_l, e, V_probe, T_e):
    return debay_l*(e*V_probe/T_e)**(3/4)'''
    
#variables
'''REGIONI
1-->Ion Saturation
a-->V_fl
2-->Transition range
b-->V_pl
3-->Electron Saturation
'''
#I_isat = corrente di saturazione ionica
#V_isat = potenziale di staurazione ionica
#I_esat = corrente di saturazione elettronica
#I_esat = potenziale di saturazione elettronica
#I_e = corrente elettronica
#V_e = potenziale elettronico
#I_probe = corrente della sonda
#V_probe = potenziale della sonda
#A_probe = area della sonda
#r_probe = raggio sonda
#A_perp = area perpendicolare a B-field
#x_g = espansione dello sheat(=guaina di schermatura)
#A_eff = area della sonda efficace 
#e = carica elettrone = 1.6*10**(-19)
#n_e = number density elettronica (parametro da ricavare)
#m_i = massa ionica = 1.66*10**(-27) (stai usando He)
#m_e = massa elettornica 
#V_pl = potenziale di plasma (parametro da ricavare)
#T_e = temperatura elettronica (parametro da ricavare)
#V_fl = potenziale di float (parametro da ricavare)
#t = tempo
#V_bias = generatore(da moltiplicare per 10)
#V_R = potenziale ai capi della resistenza
#debay_l = lunghezza di debay
#r_L_e = raggio di Larmor di elettroni
#r_L_i = raggio di Larmor di ioni
#B = campo magnetico
'''DIMENSIoNI SONDA
diametro piattello=12mm
distanza flangia-centro=180mm
'''
R=100 #Ohm #changed with file
B=107.5 #changed with file
P=0.0077 #mBar #changed with file
pos_probe=8.1 #cm #changed with file
r_probe=0.6 #cm
m_i=4*1.66*10**(-27) #4*massa_protone[Kg]
e=-1.6*10**(-19) #Coulomb

#load data
file='DSO00054.csv' #changed with file
t, V_bias, V_R=np.loadtxt(file, unpack=True, delimiter=',', skiprows=9, usecols=(3, 4, 5))
#non usi pandas perchè non riesce a leggere il file (ERROR: single positional indexer is out-of-bounds)

mask=t<0.06 #changed with data
t=t[mask]
V_bias=V_bias[mask]
V_R=V_R[mask]

#restituisce il massimo e minimo (valido anche per la funzione np.where())
#sx, dx=np.amin(V_in), np.amax(V_in)
#mask=(t>sx)&(t<dx)

#restituisce l'indice di posizione nell'array del massimo e minimo (valido anche per la funzione np.argwhere())
sx, dx=np.argmin(V_R), np.argmax(V_R)
t=t[sx:dx]
V_bias=V_bias[sx:dx]
V_R=V_R[sx:dx]

#filtering
V_bias=sig.savgol_filter(V_bias,41,3)
V_R=sig.savgol_filter(V_R,41,3)

V_probe, I_probe=(10*V_bias)-V_R, V_R/R
#10* perche oscilloscopio dimuisce di 10 volte il segnale (NB: SOLO SU ENTRATA HAI QUESTO EFFETTO)
sx, dx=np.argmin(I_probe), np.argmax(I_probe)
V_probe=V_probe[sx:dx]
I_probe=I_probe[sx:dx]

#find V_fl (momento in cui la I_probe=0)
abs_I=abs(I_probe)
val=np.argmin(abs_I)
V_fl=(V_probe[val+1]+V_probe[val-1])/2
print('Potenziale di floating: ', V_fl, 'V')

#fit range ionic saturation
mask=(I_probe>-0.0011)&(I_probe<0) #changed with data 
V_isat=V_probe[mask]
I_isat=I_probe[mask]

popt, pcov=opt.curve_fit(retta, V_isat, I_isat)
perr=np.sqrt(np.diag(pcov))
print(perr)
I_isat_opt=retta(V_isat, *popt)
print('R^2: ', r2_score(I_isat_opt, I_isat))

#fit range electronic
I_e=I_probe-retta(V_probe, *popt)
logI_e=np.log(I_e)

mask1=(V_probe>0)&(V_probe<13) #changed with data
V_e1=V_probe[mask1]
I_e1=logI_e[mask1]
popt1, pcov1=opt.curve_fit(retta, V_e1, I_e1)
perr1=np.sqrt(np.diag(pcov1))
print(perr1)
I_e1_opt=retta(V_e1, *popt1)
print('R^2: ', r2_score(I_e1_opt, I_e1))

mask2=(V_probe>9.5)&(V_probe<25) #changed with data
V_e2=V_probe[mask2]
I_e2=logI_e[mask2]
popt2, pcov2=opt.curve_fit(retta, V_e2, I_e2)
perr2=np.sqrt(np.diag(pcov2))
print(perr2)
I_e2_opt=retta(V_e2, *popt2)
print('R^2: ', r2_score(I_e2_opt, I_e2))

#find V_pl (intersezione tra le due rette)
d_m, d_q=(popt1[0]-popt2[0]), (popt1[1]-popt2[1])
V_pl=d_q/(-d_m)
err_V_pl=(abs(d_m))*np.sqrt((perr1[1])**2+(perr2[1])**2+(d_q*perr1[0]/d_m)**2+(d_q*perr2[0]/d_m)**2)
print('Potenziale di plasma: ', V_pl, '+/-', err_V_pl, 'V')

#find T_e (andamento di logI_e lineare-->m=1/T_e)
T_e=1/popt1[0] #eV
err_T_e=T_e*(perr1[0]/popt1[0])
print('Temperatura elettronica: ', T_e, '+/-', err_T_e, 'eV')
#--> 1[eV]=1[K]

#find n_e (lo trovi da regione di saturazione ionica)
I_isat_val, err_I_isat_val=popt[1], perr[1] #per V=0 la corrente ionica è q del fit ionico

#area sonda
A_probe, err_A_probe=np.pi*(r_probe**2), 0

n_e=(I_isat_val/(0.6*e*A_probe))*np.sqrt(m_i/(T_e*(-e))) #N/cm^3 
#perchè -e al denominatore?? così ottieni [J]=[Kg]*[m/s]^2 in modo tale che le unità di misure tornano 
#CONVERSIONI:  1.6*10**(-19)[J] = 1[eV] = 1[K]
err_n_e=n_e*np.sqrt((err_I_isat_val/I_isat_val)**2+(err_A_probe/A_probe)**2+(err_T_e/T_e)**2)
print('Densità elettronica: ', '{:.3e}'.format(n_e), '+/-', '{:.3e}'.format(err_n_e), 'N/cm^3')
#permette di scrivere il risultato in notazione scientifica, .3 indica quante cifre decimali mette

#stima dei parametri per la trattazione non semplificata
debay_l=743*np.sqrt(T_e/n_e) #cm
err_debay_l=debay_l*(err_T_e/T_e)

r_L_e=2.38*np.sqrt(T_e)/B #cm
err_r_L_e=r_L_e*err_T_e/T_e
r_L_i=np.sqrt(3*T_e*m_i)/B #cm
err_r_L_i=r_L_i*err_T_e/T_e

'''
if(r_L_e < r_probe*2):
    x_g=debay_l*(e*V_probe/T_e)**(3/4)
    Area_eff=A_probe*(1+x_g/r_L_e)
'''

print('Lunghezza di Debay: ', debay_l, ' +/- ', err_debay_l, 'cm')
print('Raggio di Larmor di un elettrone: ', r_L_e, ' +/- ', err_r_L_e, 'cm')
print('Raggio di Larmor di uno ione: ', r_L_i, ' +/- ', err_r_L_i, 'cm')

#fit a quattro parametri
mask=(V_probe>-40)&(V_probe<10) #changed with data
V_probe_fit=V_probe[mask]
I_probe_fit=I_probe[mask]

p_0=I_isat_val, 1, V_fl, T_e #optional(solo se non lo riesce a fare da solo)
popt_I, pcov_I=opt.curve_fit(I, V_probe_fit, I_probe_fit, p_0)
perr_I=np.sqrt(np.diag(pcov_I))

print('Parameters +/- errors')
print('Corrente ionica:', popt_I[0], '+/-', perr_I[0], 'A')
print('Alpha:', popt_I[1], '+/-', perr_I[1])
print('Potenziale di floating:', popt_I[2], '+/-', perr_I[2], 'V')
print('Temperatura elettronica:', popt_I[3], '+/-', perr_I[3], 'eV')
print('Densità elettronica: ', '{:.3e}'.format(n_e), '+/-', '{:.3e}'.format(err_n_e), 'N/cm^3')

#plot data
fig=plt.figure(figsize=(20,10))
ax1=fig.add_subplot(231).plot(t, V_bias)
plt.title('Graph V_bias')
plt.xlabel('Time (s)')
plt.ylabel('Voltage (V)')
plt.grid(linestyle='dashed')
ax2=fig.add_subplot(232).plot(t, V_R)
plt.title('Graph V_R')
plt.xlabel('Time (s)')
plt.ylabel('Voltage (V)')
plt.grid(linestyle='dashed')

#plot I-V + fit range ionic saturation
ax3=fig.add_subplot(233).plot(V_probe, I_probe, color='blue', label='Data')
plt.plot(V_isat, retta(V_isat, *popt), color='red', label='I ionic sat')
plt.title('Graph I-V + fit range ionic saturation')
plt.legend()
plt.grid(linestyle='dashed')
plt.xlabel('V probe (V)')
plt.ylabel('I probe (A)')

#plot I-V + fit range electronic
ax4=fig.add_subplot(234).plot(V_probe, logI_e, color='blue', label='Data')
plt.plot(V_e1, retta(V_e1, *popt1), color='red', label='I transition')
plt.plot(V_e2, retta(V_e2, *popt2), color='yellow', label='I electronic sat')
plt.title('Graph I-V + fit range electronic')
plt.legend()
plt.grid(linestyle='dashed')
plt.xlabel('V probe (V)')
plt.ylabel('log(I) (A)')

#plot I-V + fit 4 parametri
ax5=fig.add_subplot(235).plot(V_probe, I_probe, color='blue', label='Data')
plt.plot(V_probe_fit, I(V_probe_fit, *popt_I), color='red', label='4 Parameters')
plt.title('Graph I_V + fit 4 parameters')
plt.legend()
plt.grid(linestyle='dashed')
plt.xlabel('V probe (V)')
plt.ylabel('I probe (A)')

plt.savefig('DSO00054.png') #changed with file
plt.show()

#Algoritmo della temperature minima
n_points=50
d=(V_pl-V_fl)/n_points #piccolo range per modificare il fit
results, errors=np.empty((0,4), float), np.empty((0,4), float) #0=number of rows, 4=number of colums
for i in range(0,n_points):
    #masking data for fit:
    sx, dx=-40, V_fl+i*d #gli estremi sono quelli del fit 4 parametri
    mask=(V_probe>sx)&(V_probe<dx)
    V_probe_alg=V_probe[mask]
    I_probe_alg=I_probe[mask]

    #fitting
    popt_alg, pcov_alg=opt.curve_fit(I, V_probe_alg, I_probe_alg, popt_I, maxfev=100000)
    perr_alg=np.sqrt(np.diag(pcov_alg))

    results=np.append(results, np.array([[popt_alg[0], popt_alg[1], popt_alg[2], popt_alg[3]]]), axis=0)
    errors=np.append(errors, np.array([[perr_alg[0], perr_alg[1], perr_alg[2], perr_alg[3]]]), axis=0)
    #np.append(name_array, value, axis) --> axis=l'asse lungo la quale vengono messi, mi permette di creare la matrice

T_vect=results[:,3]
arg_T_min=np.argmin(T_vect)

best_results=results[arg_T_min, :]
best_errors=errors[arg_T_min, :]

print('Best results with algorithm')
print('Corrente ionica:', best_results[0], '+/-', best_errors[0], 'A')
print('Alpha:', best_results[1], '+/-', best_errors[1])
print('Potenziale di floating:', best_results[2], '+/-', best_errors[2], 'V')
print('Temperatura elettronica:', best_results[3], '+/-', best_errors[3], 'eV')

I_isat_alg, err_I_isat_alg=best_results[0], best_errors[0]
n_e_alg=(I_isat_alg/(0.6*e*A_probe))*np.sqrt(m_i/(T_e*(-e))) #N/cm^3
err_n_e_alg=n_e_alg*np.sqrt((err_I_isat_alg/I_isat_alg)**2+(err_A_probe/A_probe)**2+(err_T_e/T_e)**2)

print('Densità elettronica: ', '{:.3e}'.format(n_e_alg), '+/-' , '{:.3e}'.format(err_n_e_alg), 'N/cm^3')

#save result
fl=open('Results_0.0077P.txt', 'a')
#a --> permette di generare (o scrivere in coda se già esistente) il file di testo
#w --> permette di generare (o sovrascrivere se già esistente) il file di testo

#fl.write('R, B, P, pos_probe, V_fl, err_V_fl, T_e, err_T_e, n_e, err_n_e')
fl.write('\n'+str(R)+', '+str(B)+', '+str(P)+', '+str(pos_probe)+', ')
fl.write(str(best_results[2])+', '+str(best_errors[2])+', ')
fl.write(str(best_results[3])+', '+str(best_errors[3])+', ')
fl.write(str('{:.3e}'.format(n_e_alg))+', '+str('{:.3e}'.format(err_n_e_alg)))
#permette di scrivere il risultato in forma di potenza con 3 decimali

fl.close()