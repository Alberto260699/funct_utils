#library
import os
import random as rd
import string as st
import numpy as np
import matplotlib.pyplot as plt
import scipy.signal as sig
import scipy.optimize as opt
from sklearn.metrics import r2_score

#ATTENZIONE: salva in automatico devi cambiare i nomi dei salvataggi

#functions
def retta(x,m,q):
    return x*m+q

def iperbole(x,a):
    return a*(1/x)

def iperbole2(x,a):
    return a+(3.14/x**2)

def gauss(x,A,mu,sigma):
    exp = -(x-mu)**2/(2*sigma**2)
    norm = A/(np.sqrt(2*np.pi)*sigma)
    return norm*np.exp(exp)

def option0(): #calcolo area-baseline con plot ottimizzato (per prove)
    cwd=os.getcwd() #lettura directory
    os.chdir(cwd+'/gc') #scelta della directory
    var=int(input('Quale set di file vuoi leggere:' ))
    var1=int(input('Quanti sono i file:' ))

    #load data
    for i in range (1, var1+1):
        fl='_'.join([str(var).zfill(4), str(i).zfill(3)])+'.AXY'
        '''
        str(i).zfill(3) modo per scrivere il numero i in 3 cifre
        join() serve per concatenare le stringe con _ in mezzo
        ATTENTO: str() converte il numero in stringa
        '''
        x, y=np.loadtxt(fl, delimiter=',', skiprows=0, usecols=(0,1), unpack=True)
        sx, dx=0.250, 0.450
        sx1, dx1=0.290, 0.300
        sx2, dx2=0.400, 0.430
       
        #optimization limits baseline
        os.chdir(cwd+'/Base')
        f1, sf1, sx_1, dx_1, sx_2, dx_2=np.loadtxt('propano.txt', delimiter=',', skiprows=1, usecols=(0,1,2,3,4, 5), unpack=True)
        for j in range(len(open('propano.txt').readlines())-1):
            if(var==f1[j] and i==sf1[j]):
                sx1, dx1=sx_1[j], dx_1[j]
                sx2, dx2=sx_2[j], dx_2[j]
        
        mask=(x>sx)&(x<dx)
        mask1=(x>sx1)&(x<dx1)
        mask2=(x>sx2)&(x<dx2)
        x_plot=x[mask]
        y_plot=y[mask]
        x_fit=x[mask1+mask2]
        y_fit=y[mask1+mask2]
        
        #off/on plasma
        if(i==1):
            var2=1
        elif(i>1 and i<=4):
            var2=0
        elif(i>4):
            var2=1

        #fit retta
        popt, pcov=opt.curve_fit(retta, x_fit, y_fit)
        perr=np.sqrt(np.diag(pcov))
        yopt=retta(x_fit, *popt)
        print('R^2: ', r2_score(yopt, y_fit))

        #area's calculate (calibrated)
        area=0
        mask3=(x>dx1)&(x<sx2)
        x_area=x[mask]
        y_area=y[mask]
        delta_x=x_area[1]-x_area[0]
        p=[801,-8.65] #conversione da conteggio a ppm
        for j in range(len(y_area)):
            area=area+(y_area[j]-retta(x_area[j],*popt))*delta_x
        area=10**4*(area+p[1])/p[0]
        print(area)

        #parameters lecture
        os.chdir(cwd+'/Parametri')
        f, a, voc, V, I=np.loadtxt('parametri.txt', delimiter=',', skiprows=1, usecols=(0,2,3,6,7), unpack=True)
        for j in range(len(open('parametri.txt').readlines())-1): #permette di contare quante righe ci sono nel file
            if(var==int(f[j])):
                power=V[j]*I[j]
                flux=int(a[j])
        
        os.chdir(cwd+'/gc')
        #devi tornare nella cartella di inizio altrimenti il ciclo si interrompe

        #plot data
        fig=plt.figure(figsize=(10,5))
        
        ax1=fig.add_subplot(121).plot(x, y, color='blue')
        plt.xlabel('Time (min)')
        plt.ylabel('Area (ppm)')
        plt.grid(linestyle='--')

        ax2=fig.add_subplot(122).plot(x_plot,retta(x_plot,*popt),color='red',label='baseline')
        plt.plot(x_plot,y_plot,color='blue',label='plot')
        plt.xlabel('Time (min)')
        plt.ylabel('Area (ppm)')
        plt.legend()
        plt.grid(linestyle='--')
    plt.show()

#ATTENZIONE: cambiare i valori per plasma 0/I da dinamico a statico
def option1(): #calcolo area-baseline con plot ottimizzato + scrive su file 'area_results.txt'
    cwd=os.getcwd() #lettura directory
    os.chdir(cwd+'/gc') #scelta della directory
    var=int(input('Quale set di file vuoi leggere:' ))
    var1=int(input('Quanti sono i file:' ))

    #load data
    for i in range (1, var1+1):
        fl=str(var).zfill(4)+'_'+str(i).zfill(3)+'.AXY'
        '''
        str(i).zfill(3) modo per scrivere il numero i in 3 cifre
        ATTENTO: str() converte il numero in stringa
        '''
        x, y=np.loadtxt(fl, delimiter=',', skiprows=0, usecols=(0,1), unpack=True)
        sx, dx=0.250, 0.450
        sx1, dx1=0.290, 0.300
        sx2, dx2=0.400, 0.430
       
        #optimization limits baseline
        os.chdir(cwd+'/Base')
        f1, sf1, sx_1, dx_1, sx_2, dx_2=np.loadtxt('propano.txt', delimiter=',', skiprows=1, usecols=(0,1,2,3,4,5), unpack=True)
        for j in range(len(open('propano.txt').readlines())-1):
            if(var==f1[j] and i==sf1[j]):
                sx1, dx1=sx_1[j], dx_1[j]
                sx2, dx2=sx_2[j], dx_2[j]
        
        mask=(x>sx)&(x<dx)
        mask1=(x>sx1)&(x<dx1)
        mask2=(x>sx2)&(x<dx2)
        x_plot=x[mask]
        y_plot=y[mask]
        x_fit=x[mask1+mask2]
        y_fit=y[mask1+mask2]
        
        #off/on plasma flusso
        if(i==1):
            var2=1
        elif(i>1 and i<=4):
            var2=0
        elif(i>4):
            var2=1
        '''
        #off/on plasma statico
        if(i==1):
            var2=0
        elif(i>1):
            var2=1'''

        #fit retta
        popt, pcov=opt.curve_fit(retta, x_fit, y_fit)
        perr=np.sqrt(np.diag(pcov))
        yopt=retta(x_fit, *popt)
        print('R^2: ', r2_score(yopt, y_fit))

        #area's calculate (calibrated)
        area=0
        mask3=(x>dx1)&(x<sx2)
        x_area=x[mask]
        y_area=y[mask]
        delta_x=x_area[1]-x_area[0]
        p=[801,-8.65] #conversione da conteggio a ppm
        for j in range(len(y_area)):
            area=area+(y_area[j]-retta(x_area[j],*popt))*delta_x
        area=10**4*(area+p[1])/p[0]
        print(area)

        #parameters lecture
        os.chdir(cwd+'/Parametri')
        f, a, voc, V, I=np.loadtxt('parametri.txt', delimiter=',', skiprows=1, usecols=(0,2,3,6,7), unpack=True)
        for j in range(len(open('parametri.txt').readlines())-1): #permette di contare quante righe ci sono nel file
            if(var==int(f[j])):
                power=V[j]*I[j]
                flux=int(a[j])

        #save results
        os.chdir(cwd+'/Areapicchi') 
        fl1=open('area_results.txt', 'a')
        fl1.write(str(var)+', '+str((120*i)-120)+', '+str(area)+', '+str(var2)+', '+str(int(power))+', '+str(int(flux))+'\n')
        fl1.close()

        os.chdir(cwd+'/gc')
        #devi tornare nella cartella di inizio altrimenti il ciclo si interrompe

        #plot data
        fig=plt.figure(figsize=(10,5))
        
        ax1=fig.add_subplot(121).plot(x, y, color='blue')
        plt.xlabel('Time (min)')
        plt.ylabel('Area (ppm)')
        plt.grid(linestyle='--')

        ax2=fig.add_subplot(122).plot(x_plot,retta(x_plot,*popt),color='red',label='baseline')
        plt.plot(x_plot,y_plot,color='blue',label='plot')
        plt.xlabel('Time (min)')
        plt.ylabel('Area (ppm)')
        plt.legend()
        plt.grid(linestyle='--')
    plt.show()

def option2(): #plot grafici variazione concentrazione + salvataggio immagine
    #load data
    try:
        print('Inserisci i nomi dei file che vuoi plottare (premere INVIO per terminare):')
        source=[]
        while True:
            var=int(input())
            source.append(var)
            if var=='':
                break
    except ValueError:
        pass
        
    cwd=os.getcwd()
    os.chdir(cwd+'/Areapicchi')
    f, x, y, z, w=np.loadtxt('area_results.txt', delimiter=',', skiprows=1, usecols=(0,1,2,3,4), unpack=True)
    shift=360

    #plot data
    fig=plt.figure(figsize=(10,5))
    ax1=fig.add_subplot(121)
    plt.xlabel('Tempo (s)')
    plt.ylabel('Concentrazione (ppm)')

    ax2=fig.add_subplot(122)
    plt.xlabel('Tempo (s)')
    plt.ylabel('Concentrazione normalizzata')

    for i in range(len(source)):
        x_fit=x[f==source[i]]
        y_fit=y[f==source[i]]
        z_fit=z[f==source[i]]
        w_fit=w[f==source[i]]
        
        m=rd.choice('.ov^<>spP*hH+XDd1234+x') #setta marker casuali
        
        ax1.semilogy(x_fit[1:]-shift, y_fit[1:], marker=m, label=str(int(round(np.mean(y_fit[z_fit==0]),-2)))+' ppm')
        '''
        la funzione ruond arrontonda per eccesso round(numero, arrotondamento)
        0 arrotonda alle unità
        >0 arrotonda alle cifre decimi, centsimi...
        <0 arrontonda decine, centinaia...
        '''
        ax1.hlines(y=np.mean(y_fit[z_fit==0]),xmin=x_fit[1]-shift,xmax=0,color='blue')
        ax1.axvline(x=0, color='red')
        ax1.legend(loc='lower left')
        ax1.grid(True, which='both', linestyle='--') #devi scrivere così per avere la griglia nel grafico logaritmici
        ax1.set_ylim(200,10000)
        ax1.text(-200, 7200, 'Plasma off')
        ax1.text(109, 280, 'Plasma on')

        ax2.errorbar(x_fit[1:]-shift, y_fit[1:]/np.mean(y_fit[z_fit==0]), marker=m)
        ax2.axvline(x=0, color='red')
        ax2.set_ylim(0.3,1.15)
        ax2.text(-200, 0.68, 'Plasma off')
        ax2.text(109, 0.88, 'Plasma on')
        ax2.grid(which='both', linestyle='--') #which='both', axis='both' opzionali nel caso non ti fa la griglia come vuoi

    os.chdir(cwd+'/Immagini')
    #plt.savefig('Cambio_concentrazione_'+str(int(w_fit[0]))+'.png')
    plt.show()

def option3(): #plot grafici variazione flussi + salavataggio immagine
    #load data
    try:
        print('Inserisci i nomi dei file che vuoi plottare (premere INVIO per terminare):')
        source=[]
        while True:
            var=int(input())
            source.append(var)
            if var=='':
                break
    except ValueError:
        pass

    cwd=os.getcwd()
    os.chdir(cwd+'/Areapicchi')
    f, x, y, z, w=np.loadtxt('area_results.txt', delimiter=',', skiprows=1, usecols=(0,1,2,3,5), unpack=True)
    shift=360

    #plot data
    fig=plt.figure(figsize=(10,5))
    ax1=fig.add_subplot(121)
    plt.xlabel('Tempo (s)')
    plt.ylabel('Concentrazione (ppm)')

    ax2=fig.add_subplot(122)
    plt.xlabel('Tempo (s)')
    plt.ylabel('Concentrazione normalizzata')

    for i in range(len(source)):
        x_fit=x[f==source[i]]
        y_fit=y[f==source[i]]
        z_fit=z[f==source[i]]
        w_fit=w[f==source[i]]
        
        m=rd.choice('.ov^<>spP*hH+XDd1234+x') #setta marker casuali
        
        ax1.semilogy(x_fit[1:]-shift, y_fit[1:], marker=m, label=str(int(w_fit[0]))+' L/min')
        ax1.hlines(y=np.mean(y_fit[z_fit==0]),xmin=x_fit[1]-shift,xmax=0, color='blue') #plot linea corrispondente alla media dei primi 4 valori
        ax1.axvline(x=0, color='red')
        ax1.legend(loc='lower left')
        ax1.grid(True, which='both', linestyle='--') #devi scrivere così per avere la griglia nel grafico logaritmico
        ax1.set_ylim(600,2000)
        ax1.text(-200, 1590, 'Plasma off')
        ax1.text(109, 1590, 'Plasma on')

        ax2.errorbar(x_fit[1:]-shift, y_fit[1:]/np.mean(y_fit[z_fit==0]), marker=m)
        ax2.axvline(x=0, color='red')
        ax2.set_ylim(0.3,1.15)
        ax2.text(-200, 0.68, 'Plasma off')
        ax2.text(109, 0.88, 'Plasma on')
        ax2.grid(which='both', linestyle='--') #which='both', axis='both' opzionali nel caso non ti fa la griglia come vuoi

    os.chdir(cwd+'/Immagini')
    #plt.savefig('Cambio_flussi_90.png')
    plt.show()

def option4(): #plot grafici variazione potenza + salavataggio immagine
    #load data
    try:
        print('Inserisci i nomi dei file che vuoi plottare (premere INVIO per terminare):')
        source=[]
        while True:
            var=int(input())
            source.append(var)
            if var=='':
                break
    except ValueError:
        pass 

    cwd=os.getcwd()
    os.chdir(cwd+'/Areapicchi')
    f, x, y, z, w=np.loadtxt('area_results.txt', delimiter=',', skiprows=1, usecols=(0,1,2,3,4), unpack=True)
    shift=360

    #plot data
    fig=plt.figure(figsize=(10,5))
    ax1=fig.add_subplot(121)
    plt.xlabel('Tempo (s)')
    plt.ylabel('Concentrazione (ppm)')
    
    ax2=fig.add_subplot(122)
    plt.xlabel('Tempo (s)')
    plt.ylabel('Concentrazione normalizzata')

    for i in range(len(source)):
        x_fit=x[f==source[i]]
        y_fit=y[f==source[i]]
        z_fit=z[f==source[i]]
        w_fit=w[f==source[i]]
        
        m=rd.choice('.ov^<>spP*hH+XDd1234+x') #setta marker casuali
        
        ax1.semilogy(x_fit[1:]-shift, y_fit[1:], marker=m, label=str(int(w_fit[0]))+' W')
        ax1.hlines(y=np.mean(y_fit[z_fit==0]),xmin=x_fit[1]-shift,xmax=0, color='blue') #plot linea corrispondente alla media dei primi 4 valori
        ax1.axvline(x=0, color='red')
        ax1.legend(loc='lower left')
        ax1.grid(True, which='both', linestyle='--') #devi scrivere così per avere la griglia nel grafico logaritmico
        ax1.set_ylim(500,2000)
        ax1.text(-200, 1180, 'Plasma off')
        ax1.text(150, 1360, 'Plasma on')

        ax2.errorbar(x_fit[1:]-shift, y_fit[1:]/np.mean(y_fit[z_fit==0]), marker=m)
        ax2.axvline(x=0, color='red')
        ax2.set_ylim(0.3,1.15)
        ax2.text(-200, 0.68, 'Plasma off')
        ax2.text(150, 0.88, 'Plasma on')
        ax2.grid(which='both', linestyle='--') #which='both', axis='both' opzionali nel caso non ti fa la griglia come vuoi

    os.chdir(cwd+'/Immagini')
    #plt.savefig('Cambio_potenza.png')
    plt.show()

def option5(): #plot grafici flussi 2:8 per potenze 40,90W + salvataggio immagine
    #load data
    var=int(input('Quanti file vuoi plottare:'))
    print('Insersci il nome del file:')
    source=[]
    for i in range(var):
        var1=int(input())
        source.append(var1) 

    cwd=os.getcwd()
    os.chdir(cwd+'/Areapicchi')
    f, x, y, z, w=np.loadtxt('area_results.txt', delimiter=',', skiprows=1, usecols=(0,1,2,3,4), unpack=True)
    shift=330

    #plot data
    fig=plt.figure(figsize=(10,5))
    ax1=fig.add_subplot(121)
    plt.xlabel('Time (s)')
    plt.ylabel('Concentration (ppm)')
    plt.title('Fit 90W, flussi 2:8')
    
    ax2=fig.add_subplot(122)
    plt.xlabel('Time (s)')
    plt.ylabel('Normalized concentration')

    for i in range(len(source)):
        x_fit=x[f==source[i]]
        y_fit=y[f==source[i]]
        z_fit=z[f==source[i]]
        w_fit=w[f==source[i]]
        
        m=rd.choice('.ov^<>spP*hH+XDd1234+x') #setta marker casuali
        
        ax1.semilogy(x_fit-shift, y_fit, marker=m, label=str(int(round(np.mean(y_fit[z_fit==0]),-2)))+' ppm')
        ax1.axhline(y=np.mean(y_fit[z_fit==0]), color='blue') #plot linea corrispondente alla media dei primi 4 valori
        ax1.axvline(x=0, color='red')
        ax1.legend()
        ax1.grid(True, which='both', linestyle='--') #devi scrivere così per avere la griglia nel grafico logaritmico
        ax1.set_ylim(600,2000)
        ax1.text(-270, 1180, 'Plasma off')
        ax1.text(150, 1360, 'Plasma on')

        ax2.errorbar(x_fit-shift, y_fit/np.mean(y_fit[z_fit==0]), marker=m)
        ax2.axvline(x=0, color='red')
        ax2.set_ylim(0.3,1.15)
        ax2.text(-270, 0.68, 'Plasma off')
        ax2.text(150, 0.88, 'Plasma on')
        ax2.grid(which='both', linestyle='--') #which='both', axis='both' opzionali nel caso non ti fa la griglia come vuoi

    os.chdir(cwd+'/Immagini')
    #plt.savefig('90W.png')
    plt.show()

def option6(): #plot grafici Concentrazione normalizzata vs flux/conc/power + salvataggio immagine
    #load data
    var=int(input('Quanti file vuoi plottare:'))
    print('Insersci il nome del file:')
    source=[]
    for i in range(var):
        var1=int(input())
        source.append(var1)
        
    cwd=os.getcwd()
    os.chdir(cwd+'/Areapicchi')
    
    #choose of plot
    var1=input('Cosa vuoi plottare? conc/flux/power: ')
    if(var1=='conc'):
        f, x, y, z, w=np.loadtxt('area_results.txt', delimiter=',', skiprows=1, usecols=(0,1,2,3,4), unpack=True)

        #plot data
        plt.figure()
        plt.xlabel('Concentration (ppm)')
        plt.ylabel('Normalized concentration')

        for i in range(len(source)):
            x_fit=x[f==source[i]]
            y_fit=y[f==source[i]]
            z_fit=z[f==source[i]]
            w_fit=w[f==source[i]]
            
            mean=np.mean(y_fit[x_fit>=550]/np.mean(y_fit[z_fit==0]))
            sigma=np.std(y_fit[x_fit>=550]/np.mean(y_fit[z_fit==0]))
            if(sigma==float(0)):
                sigma=np.std(y_fit[x_fit>=440]/np.mean(y_fit[z_fit==0]))
            print(mean,',',sigma)
            
            plt.errorbar(round(np.mean(y_fit[z_fit==0]),-2), mean, sigma, marker='o', capsize=4, label=str(int(round(np.mean(y_fit[z_fit==0]),-2)))+' ppm')
            
        os.chdir(cwd+'/Immagini')
        plt.xscale('log')
        plt.grid(which='both', linestyle='--')
        plt.legend()
        #plt.savefig('Norm_conc_40.png')
        plt.show()

    elif(var1=='flux'):
        f, x, y, z, w=np.loadtxt('area_results.txt', delimiter=',', skiprows=1, usecols=(0,1,2,3,5), unpack=True)

        #plot data
        plt.figure()
        plt.xlabel('Flux (L/min)')
        plt.ylabel('Normalized concentration')
        
        for i in range(len(source)):
            x_fit=x[f==source[i]]
            y_fit=y[f==source[i]]
            z_fit=z[f==source[i]]
            w_fit=w[f==source[i]]
            
            mean=np.mean(y_fit[x_fit>=550]/np.mean(y_fit[z_fit==0]))
            sigma=np.std(y_fit[x_fit>=550]/np.mean(y_fit[z_fit==0]))
            if(sigma==float(0)):
                sigma=np.std(y_fit[x_fit>=440]/np.mean(y_fit[z_fit==0]))
            print(mean,',',sigma)
            
            plt.errorbar(w_fit[0], mean, sigma, marker='o', capsize=4, label=str(int(w_fit[0]))+' L/min')

        os.chdir(cwd+'/Immagini')
        plt.grid(linestyle='--')
        plt.legend()
        #plt.savefig('Norm_flux_40.png')
        plt.show()

    elif(var1=='power'):
        f, x, y, z, w=np.loadtxt('area_results.txt', delimiter=',', skiprows=1, usecols=(0,1,2,3,4), unpack=True)

        #plot data
        plt.figure()
        plt.xlabel('Power (W)')
        plt.ylabel('Normalized concentration')
        
        for i in range(len(source)):
            x_fit=x[f==source[i]]
            y_fit=y[f==source[i]]
            z_fit=z[f==source[i]]
            w_fit=w[f==source[i]]
            
            mean=np.mean(y_fit[x_fit>=550]/np.mean(y_fit[z_fit==0]))
            sigma=np.std(y_fit[x_fit>=550]/np.mean(y_fit[z_fit==0]))
            print(mean,',',sigma)
            
            plt.errorbar(w_fit[0], mean, sigma, marker='o', capsize=4, label=str(int(w_fit[0]))+' W')

        os.chdir(cwd+'/Immagini')
        plt.grid(linestyle='--')
        plt.legend()
        #plt.savefig('Norm_power.png')
        plt.show()

#modo 1 per combinare i plot (ELEGANTE e FUNZIONALE)
def option7(): #combinazione dei plot per conc/flux/power + salvataggio immagine
    #load data
    try:
        print('Inserisci i nomi dei file che vuoi plottare:')
        source=[]
        run=True
        while run==True:
            var=int(input())
            source.append(var)
            if var=='':
                break
    except ValueError:
        pass
        
    cwd=os.getcwd()
    os.chdir(cwd+'/Areapicchi')
    
    #choose of plot
    var1=input('Cosa vuoi plottare? conc/flux/power: ')
    if(var1=='conc'):
        f, x, y, z, w=np.loadtxt('area_results.txt', delimiter=',', skiprows=1, usecols=(0,1,2,3,4), unpack=True)

        #plot data
        plt.figure()
        plt.xlabel('Concentrazione (ppm)')
        plt.ylabel('Concentrazione normalizzata')
    
        matrix=np.empty((0,4),float)
        power=[]
        
        for i in range(len(source)):
            x_fit=x[f==source[i]]
            y_fit=y[f==source[i]]
            z_fit=z[f==source[i]]
            w_fit=w[f==source[i]]
                            
            sigma=np.std(y_fit[x_fit>=550]/np.mean(y_fit[z_fit==0]))
            if(sigma==float(0)):
                matrix=np.append(matrix, np.array([[round(np.mean(y_fit[z_fit==0]),-2), np.mean(y_fit[x_fit>=440])/np.mean(y_fit[z_fit==0]), np.std(y_fit[x_fit>=440]/np.mean(y_fit[z_fit==0])), w_fit[0]]]), axis=0)
            else:
                matrix=np.append(matrix, np.array([[round(np.mean(y_fit[z_fit==0]),-2), np.mean(y_fit[x_fit>=550])/np.mean(y_fit[z_fit==0]), np.std(y_fit[x_fit>=550]/np.mean(y_fit[z_fit==0])), w_fit[0]]]), axis=0)
            
            if w_fit[0] in power:
                continue #si usa per skippare tutto il resto del loop
                power.append(w_fit[0])
            
            
        print(matrix)
        for i in range(len(power)):
            matrix1=matrix[matrix[:,3]==power[i]]
            print(matrix1)
            plt.errorbar(matrix1[:,0], matrix1[:,1], matrix1[:,2], marker='o', capsize=4, linestyle='-.', label=str(int(matrix1[0,3]))+' W')
            
        os.chdir(cwd+'/Immagini')
        plt.xscale('log')
        plt.grid(which='both', linestyle='--')
        plt.legend()
        plt.savefig('Norm_conc.png')
        plt.show()

    elif(var1=='flux'):
        f, x, y, z, w, q=np.loadtxt('area_results.txt', delimiter=',', skiprows=1, usecols=(0,1,2,3,4,5), unpack=True)

        #plot data
        plt.figure()
        plt.xlabel('Flusso (L/min)')
        plt.ylabel('Concentrazione normalizzata')
       
        matrix=np.empty((0,4),float)
        power=[]
        t=np.arange(2,10,0.1)
        
        for i in range(len(source)):
            x_fit=x[f==source[i]]
            y_fit=y[f==source[i]]
            z_fit=z[f==source[i]]
            w_fit=w[f==source[i]]
            q_fit=q[f==source[i]]
            
            sigma=np.std(y_fit[x_fit>=550]/np.mean(y_fit[z_fit==0]))
            if(sigma==float(0)):
                matrix=np.append(matrix, np.array([[q_fit[0], np.mean(y_fit[x_fit>=440])/np.mean(y_fit[z_fit==0]), np.std(y_fit[x_fit>=440]/np.mean(y_fit[z_fit==0])), w_fit[0]]]), axis=0)
            else:
                matrix=np.append(matrix, np.array([[q_fit[0], np.mean(y_fit[x_fit>=550])/np.mean(y_fit[z_fit==0]), np.std(y_fit[x_fit>=550]/np.mean(y_fit[z_fit==0])), w_fit[0]]]), axis=0)
            
            if w_fit[0] in power:
                continue
                power.append(w_fit[0])
            
        print(matrix)
        for i in range(len(power)):
            matrix1=matrix[matrix[:,3]==power[i]]
            print(matrix1)
            plt.errorbar(matrix1[:,0], matrix1[:,1], matrix1[:,2], marker='o', capsize=4, linestyle='-.', label=str(int(matrix1[0,3]))+' W')
            popt, pcov=opt.curve_fit(retta, matrix1[:,0], matrix1[:,1])
            plt.plot(t, retta(t, *popt))
        
        os.chdir(cwd+'/Immagini')
        plt.grid(linestyle='--')
        plt.legend()
        #plt.savefig('Norm_flux.png')
        plt.show()

    elif(var1=='power'):
        f, x, y, z, w=np.loadtxt('area_results.txt', delimiter=',', skiprows=1, usecols=(0,1,2,3,4), unpack=True)

        #plot data
        plt.figure()
        plt.xlabel('Potenza (W)')
        plt.ylabel('Concentrazione normalizzata')
    
        matrix=np.empty((0,3),float)
        power=[]
        t=np.arange(3.5,10.5,0.1)
        
        for i in range(len(source)):
            x_fit=x[f==source[i]]
            y_fit=y[f==source[i]]
            z_fit=z[f==source[i]]
            w_fit=w[f==source[i]]
                            
            sigma=np.std(y_fit[x_fit>=550]/np.mean(y_fit[z_fit==0]))
            if(sigma==float(0)):
                matrix=np.append(matrix, np.array([[w_fit[0], np.mean(y_fit[x_fit>=440])/np.mean(y_fit[z_fit==0]), np.std(y_fit[x_fit>=440]/np.mean(y_fit[z_fit==0]))]]), axis=0)
            else:
                matrix=np.append(matrix, np.array([[w_fit[0], np.mean(y_fit[x_fit>=550])/np.mean(y_fit[z_fit==0]), np.std(y_fit[x_fit>=550]/np.mean(y_fit[z_fit==0]))]]), axis=0)
            
        print(matrix)
        plt.errorbar(matrix[:,0], 1-matrix[:,1], matrix[:,2], marker='o', capsize=4, linestyle='-.')
        #popt, pcov=opt.curve_fit(iperbole2, matrix[:,0], 1-matrix[:,1])
        #print(popt)
        #plt.plot(10*(t-0.5), iperbole2(t, *popt)+0.03)
       
        os.chdir(cwd+'/Immagini')
        plt.grid(which='both', linestyle='--')
        #plt.savefig('Norm_power1.png')
        plt.show()

#modo 2 per combinare i plot (FUNZIONALE e LENTO)
def option8(): #plot grafici Efficienza Energetica vs flux/conc/power + salvataggio immagine + scrive su file 'result_conc.txt', 'result_flux.txt'
    #load data
    try:
        print('Inserisci i nomi dei file che vuoi plottare:')
        source=[]
        run=True
        while run==True:
            var=int(input())
            source.append(var)
            if var=='':
                break
    except ValueError:
        pass
        
    cwd=os.getcwd()
    os.chdir(cwd+'/Areapicchi')
    
    M=44.1 #massa molare propano
    V=24.45 #volume molare dei gas a 20°C
    
    #choose of plot
    var1=input('Cosa vuoi plottare? conc/flux/power: ')
    if(var1=='conc'):
        f, x, y, z, w, q=np.loadtxt('area_results.txt', delimiter=',', skiprows=1, usecols=(0,1,2,3,4,5), unpack=True)

        #plot data
        plt.figure()
        plt.xlabel('Concentration (ppm)')
        plt.ylabel('Energy yield (g/kWh)')
        
        for i in range(len(source)):
            x_fit=x[f==source[i]]
            y_fit=y[f==source[i]]
            z_fit=z[f==source[i]]
            w_fit=w[f==source[i]]
            q_fit=q[f==source[i]]
            
            EY=(M*(np.mean(y_fit[z_fit==0])-np.mean(y_fit[x_fit>=550]))*q_fit[0]*60)/(w_fit[0]*V*1000)
            err_EY=np.sqrt((np.var(y_fit[z_fit==0])+np.var(y_fit[x_fit>=550]))*((M*q_fit[0]*60)/(w_fit[0]*1000))**2)
            if(np.var(y_fit[x_fit>=550])==float(0)):
                err_EY=np.sqrt((np.var(y_fit[z_fit==0])+np.var(y_fit[x_fit>=440]))*((M*q_fit[0]*60)/(w_fit[0]*1000))**2)
            print(EY,',',err_EY)
            
            plt.errorbar(round(np.mean(y_fit[z_fit==0]),-2), EY, err_EY, marker='o', capsize=4, label=str(int(round(np.mean(y_fit[z_fit==0]),-2)))+' ppm')
            
            #save results for combination
            fl=open('result_conc.txt', 'a')
            fl.write(str(round(np.mean(y_fit[z_fit==0]),-2))+', '+str(EY)+', '+str(err_EY)+', '+str(w_fit[0])+'\n')
            fl.close()
            

        os.chdir(cwd+'/Immagini')
        plt.xscale('log')
        plt.grid(which='both', linestyle='--')
        plt.legend()
        #plt.savefig('EY_conc_30.png')
        plt.show()

    elif(var1=='flux'):
        f, x, y, z, w, q=np.loadtxt('area_results.txt', delimiter=',', skiprows=1, usecols=(0,1,2,3,4,5), unpack=True)

        #plot data
        plt.figure()
        plt.xlabel('Flux (L/min)')
        plt.ylabel('Energy yield (g/kWh)')
        
        for i in range(len(source)):
            x_fit=x[f==source[i]]
            y_fit=y[f==source[i]]
            z_fit=z[f==source[i]]
            w_fit=w[f==source[i]]
            q_fit=q[f==source[i]]
            
            EY=(M*(np.mean(y_fit[z_fit==0])-np.mean(y_fit[x_fit>=550]))*q_fit[0]*60)/(w_fit[0]*V*1000)
            err_EY=np.sqrt((np.var(y_fit[z_fit==0])+np.var(y_fit[x_fit>=550]))*((M*q_fit[0]*60)/(w_fit[0]*1000))**2)
            if(np.var(y_fit[x_fit>=550])==float(0)):
                err_EY=np.sqrt((np.var(y_fit[z_fit==0])+np.var(y_fit[x_fit>=440]))*((M*q_fit[0]*60)/(w_fit[0]*1000))**2)
            print(EY,',',err_EY)
            
            plt.errorbar(q_fit[0], EY, err_EY, marker='o', capsize=4, label=str(int(q_fit[0]))+' L/min')
            
            #save results for combination
            fl=open('result_flux.txt', 'a')
            fl.write(str(q_fit[0])+', '+str(EY)+', '+str(err_EY)+', '+str(w_fit[0])+'\n')
            fl.close()
            

        os.chdir(cwd+'/Immagini')
        plt.grid(linestyle='--')
        plt.legend()
        #plt.savefig('EY_flux_40.png')
        plt.show()

    elif(var1=='power'):
        f, x, y, z, w, q=np.loadtxt('area_results.txt', delimiter=',', skiprows=1, usecols=(0,1,2,3,4,5), unpack=True)

        #plot data
        plt.figure()
        plt.xlabel('Power (W)')
        plt.ylabel('Energy yield (g/kWh)')
        
        for i in range(len(source)):
            x_fit=x[f==source[i]]
            y_fit=y[f==source[i]]
            z_fit=z[f==source[i]]
            w_fit=w[f==source[i]]
            q_fit=q[f==source[i]]
            
            EY=(M*(np.mean(y_fit[z_fit==0])-np.mean(y_fit[x_fit>=550]))*q_fit[0]*60)/(w_fit[0]*V*1000)
            err_EY=np.sqrt((np.var(y_fit[z_fit==0])+np.var(y_fit[x_fit>=550]))*((M*q_fit[0]*60)/(w_fit[0]*1000))**2)
            print(EY,',',err_EY)
            
            plt.errorbar(w_fit[0], EY, err_EY, marker='o', capsize=4, label=str(int(w_fit[0]))+' W')
            
            #save results for combination
            fl=open('result_power.txt', 'a')
            fl.write(str(w_fit[0])+', '+str(EY)+', '+str(err_EY)+'\n')
            fl.close()

        os.chdir(cwd+'/Immagini')
        plt.grid(linestyle='--')
        plt.legend()
        #plt.savefig('EY_power.png')
        plt.show()

def option9(): #combinazione dei plot per conc/flux/power + salvataggio immagine
    #load data
    var1=input('Cosa vuoi plottare? conc/flux/power: ')
    
    cwd=os.getcwd()
    os.chdir(cwd+'/Areapicchi')
    
    #choose of plot
    if(var1=='conc'):
        try:
            print('Inserisci le potenze che vuoi plottare:')
            source=[]
            run=True
            while run==True:
                var=int(input())
                source.append(var)
                if var=='':
                    break
        except ValueError:
            pass
            
        x, y, err_y, w=np.loadtxt('result_conc.txt', delimiter=',', skiprows=1, usecols=(0,1,2,3), unpack=True)
        
        plt.figure()
        plt.xlabel('Concentrazione (ppm)')
        plt.ylabel('Efficienza energetica (g/kWh)')
        
        for i in range(len(source)):
            x_fit=x[w==source[i]]
            y_fit=y[w==source[i]]
            err_fit=err_y[w==source[i]]
            
            m=rd.choice('.ov^<>spP*hH+XDd1234+x')
            plt.errorbar(x_fit, y_fit, err_fit, marker=m, capsize=4, linestyle='-.', label=str(int(source[i]))+' W')
        
        os.chdir(cwd+'/Immagini')
        plt.xscale('log')
        plt.grid(which='both', linestyle='--')
        plt.legend()
        plt.savefig('EY_conc.png')
        plt.show()
    
    elif(var1=='flux'):
        try:
            print('Inserisci le potenze che vuoi plottare:')
            source=[]
            run=True
            while run==True:
                var=int(input())
                source.append(var)
                if var=='':
                    break
        except ValueError:
            pass
            
        x, y, err_y, w=np.loadtxt('result_flux.txt', delimiter=',', skiprows=1, usecols=(0,1,2,3), unpack=True)
        
        plt.figure()
        plt.xlabel('Flussi (L/min)')
        plt.ylabel('Efficienza Energetica (g/kWh)')
        
        for i in range(len(source)):
            x_fit=x[w==source[i]]
            y_fit=y[w==source[i]]
            err_fit=err_y[w==source[i]]
            
            m=rd.choice('.ov^<>spP*hH+XDd1234+x')
            plt.errorbar(x_fit, y_fit, err_fit, marker=m, capsize=4, linestyle='-.', label=str(int(source[i]))+' W')
    
        os.chdir(cwd+'/Immagini')
        plt.grid(linestyle='--')
        plt.legend()
        plt.savefig('EY_flux.png')
        plt.show()
        
    elif(var1=='power'):
        x, y, err_y=np.loadtxt('result_power.txt', delimiter=',', skiprows=1, usecols=(0,1,2), unpack=True)
        
        plt.figure()
        plt.xlabel('Potenza (W)')
        plt.ylabel('Efficienza energetica (g/kWh)')
        
        plt.errorbar(x, y, err_y, marker='o', capsize=4, linestyle='-.')
    
        os.chdir(cwd+'/Immagini')
        plt.grid(linestyle='--')
        plt.savefig('EY_power1.png')
        plt.show()

def option10(): #plot grafici (statico)
    #load data
    try:
        print('Inserisci i nomi dei file che vuoi plottare:')
        source=[]
        run=True
        while run==True:
            var=int(input())
            source.append(var)
            if var=='':
                break
    except ValueError:
        pass
        
    cwd=os.getcwd()
    os.chdir(cwd+'/Areapicchi')
    f, x, y, z, w=np.loadtxt('area_results.txt', delimiter=',', skiprows=1, usecols=(0,1,2,3,4), unpack=True)
    name=['plasma off','plasma on']
    
    #plot data
    fig=plt.figure(figsize=(10,5))
    ax1=fig.add_subplot(121)
    plt.xlabel('Tempo (s)')
    plt.ylabel('Concentrazione (ppm)')

    ax2=fig.add_subplot(122)
    plt.xlabel('Tempo (s)')
    plt.ylabel('Concentrazione normalizzata')

    for i in range(len(source)):
        x_fit=x[f==source[i]]
        y_fit=y[f==source[i]]
        z_fit=z[f==source[i]]
        w_fit=w[f==source[i]]
        
        m=rd.choice('.ov^<>spP*hH+XDd1234+x') #setta marker casuali
        
        ax1.semilogy(x_fit, y_fit, marker=m, label=name[i])
        ax1.legend()
        ax1.grid(which='both', linestyle='--') #devi scrivere così per avere la griglia nel grafico logaritmici

        ax2.errorbar(x_fit, y_fit/y_fit[0], marker=m)
        ax2.grid(which='both', linestyle='--') #which='both', axis='both' opzionali nel caso non ti fa la griglia come vuoi

    os.chdir(cwd+'/Immagini')
    plt.savefig('Statico_30.png')
    plt.show()

#modo 3 per combinare i plot 
def option11(): #plot grafici Resa Energetica vs time (statico)
    #load data
    try:
        print('Inserisci i nomi dei file che vuoi plottare:')
        source=[]
        run=True
        while run==True:
            var=int(input())
            source.append(var)
            if var=='':
                break
    except ValueError:
        pass
        
    cwd=os.getcwd()
    os.chdir(cwd+'/Areapicchi')
    
    M=44.1 #massa molare propano
    V=24.45 #volume molare dei gas a 20°C
    vol=1.6/1000 #volume m^3
    time=110/3600 #s->h

    f, x, y, z, w=np.loadtxt('area_results.txt', delimiter=',', skiprows=1, usecols=(0,1,2,3,4), unpack=True)

    #plot data
    plt.figure()
    plt.xlabel('Tempo (s)')
    plt.ylabel('Efficienza energetica (g/kWh)')
    
    for i in range(len(source)):
        x_fit=x[f==source[i]]
        y_fit=y[f==source[i]]
        z_fit=z[f==source[i]]
        w_fit=w[f==source[i]]
        EY=[]
        
        for j in range(len(x_fit)):
            EY.append(((y_fit[0]-y_fit[j])*M*vol)/(w_fit[0]*j*time*V))
            
    plt.errorbar(x_fit, EY, marker='o', capsize=4, linestyle='-.')
    print(EY)
        
    os.chdir(cwd+'/Immagini')
    plt.grid(which='both', linestyle='--')
    plt.savefig('EY_conc_30_statico.png')
    plt.show()

def option12(): #plot grafici (confornto tubo basetta)(statico)
    #load data
    try:
        print('Inserisci i nomi dei file che vuoi plottare:')
        source=[]
        run=True
        while run==True:
            var=int(input())
            source.append(var)
            if var=='':
                break
    except ValueError:
        pass
        
    cwd=os.getcwd()
    os.chdir(cwd+'/Areapicchi')
    f, x, y, z, w=np.loadtxt('area_results.txt', delimiter=',', skiprows=1, usecols=(0,1,2,3,4), unpack=True)
    x1, y1=np.loadtxt('confronto_basetta.txt', skiprows=1, usecols=(0,1), unpack=True)
    x1=x1*60
    
    #plot data
    plt.figure()
    plt.xlabel('Time (s)')
    plt.ylabel('Normalized concentration')

    for i in range(len(source)):
        x_fit=x[f==source[i]]
        y_fit=y[f==source[i]]
        z_fit=z[f==source[i]]
        w_fit=w[f==source[i]]
        
        plt.errorbar(x_fit, y_fit/y_fit[0], marker='o', label='Tubo cilindrico', linestyle='-.')
        plt.errorbar(x1, y1, marker='o', label='Basetta piana', linestyle='-.')
        plt.grid(which='both', linestyle='--') #which='both', axis='both' opzionali nel caso non ti fa la griglia come vuoi

    os.chdir(cwd+'/Immagini')
    plt.legend()
    plt.savefig('tubo_basetta.png')
    plt.show()

def option13(): #plot con zoom di una particolare regione del grafico
    #load data
    try:
        print('Inserisci i nomi dei file che vuoi plottare:')
        source=[]
        run=True
        while run==True:
            var=int(input())
            source.append(var)
            if var=='':
                break
    except ValueError:
        pass

    try:
        print('Quali sotto-file vuoi leggere:')
        source1=[]
        run=True
        while run==True:
            var1=int(input())
            source1.append(var1)
            if var1=='':
                break
    except ValueError:
        pass

    cwd=os.getcwd()
    os.chdir(cwd+'/gc')
    fig=plt.figure()
    ax1=fig.add_subplot(111)
    plt.xlabel('Retention time (s)')
    plt.ylabel('GC Trace (counts/s)')
    plt.grid(linestyle='--')
    
    b1=[0.2, 0.7, 0.2, 0.2]
    axins1=ax1.inset_axes(b1)
    axins1.set_title('CO_2')
    axins1.set_xlim(8, 10)
    axins1.set_ylim(-100, 5.26*10**6)
    ax1.indicate_inset_zoom(axins1, edgecolor="r")
    
    b2=[0.5, 0.7, 0.2, 0.2]
    axins2=ax1.inset_axes(b2)
    axins2.set_title('Acetylene')
    axins2.set_xlim(10, 11.25)
    axins2.set_ylim(6*10**3, 1.2*10**5)
    ax1.indicate_inset_zoom(axins2, edgecolor="b")
    
    b3=[0.75, 0.45, 0.2, 0.2]
    axins3=ax1.inset_axes(b3)
    axins3.set_title('Propane')
    axins3.set_xlim(17, 22)
    axins3.set_ylim(4*10**3, 3*10**4)
    ax1.indicate_inset_zoom(axins3, edgecolor="m")
    
    b4=[0.75, 0.15, 0.2, 0.2]
    axins4=ax1.inset_axes(b4)
    axins4.set_title('Water')
    axins4.set_xlim(35, 42)
    axins4.set_ylim(1500, 1.5*10**4)
    ax1.indicate_inset_zoom(axins4, edgecolor="g")
    
    fig1=plt.figure()
    ax2=fig1.add_subplot(111, projection='3d')
    ax2.set_xlabel('t (s)')
    ax2.set_ylabel('Retention time (s)')
    ax2.set_zlabel('GC Trace (counts/s)')

    for i in range(10):
        for j in range(len(source1)):
            if(i==source1[j]):
                fl=str(var).zfill(4)+'_'+str(i).zfill(3)+'.AXY'
                x, y=np.loadtxt(fl, delimiter=',', skiprows=0, usecols=(0,1), unpack=True)
                ax1.plot(x*60,y,label='t='+str((i-1)*120)+' s')
                axins1.plot(x*60,y)
                axins2.plot(x*60,y)
                axins3.plot(x*60,y)
                axins4.plot(x*60,y)
                
                ax2.scatter((i-1)*120,x*60,y,label='t='+str((i-1)*120)+' s')

    ax1.legend()
    plt.show()

def option(): #plot grafici ?? doppio label
    #load data
    var=int(input('Quanti file vuoi plottare:'))
    print('Insersci il nome del file:')
    source=[]
    for i in range(var):
        var1=int(input())
        source.append(var1) 

    cwd=os.getcwd()
    os.chdir(cwd+'/Areapicchi')
    f, x, y, z, w=np.loadtxt('area_results.txt', delimiter=',', skiprows=1, usecols=(0,1,2,3,4), unpack=True)
    shift=330

    #plot data
    fig=plt.figure()
    ax1=fig.add_subplot(111)
    plt.xlabel('Time (s)')
    plt.ylabel('Concentration (ppm)')
    
    ax2=ax1.twinx() #serve per plottare i dati sullo stesso grafico
    plt.ylabel('Normalized concentration')

    for i in range(len(source)):
        x_fit=x[f==source[i]]
        y_fit=y[f==source[i]]
        z_fit=z[f==source[i]]
        w_fit=w[f==source[i]]
        
        m=rd.choice('.ov^<>spP*hH+XDd1234+x') #setta marker casuali
        
        ax1.errorbar(x_fit-shift, y_fit, 0.1, marker=m, label=str(int(w_fit[0]))+' W')
        ax1.axhline(y=np.mean(y_fit[z_fit==0]), color='blue') #plot linea corrispondente alla media dei primi 4 valori
        ax1.axvline(x=0, color='red')
        ax1.legend()
        ax1.grid(True, which='both', linestyle='--') #devi scrivere così per avere la griglia nel grafico logaritmico
        #ax1.set_ylim(500,10000)
        ax1.text(-270, 1180, 'Plasma off')
        ax1.text(150, 1360, 'Plasma on')
        
        #ax2.set_ylim(0.3,1.15)
       
    os.chdir(cwd+'/Immagini')
    #plt.savefig('Cambio_potenza.png')
    plt.show()

def option():#se devi inserire valori da tastiera senza usare for/salvataggio cambio nome autonomo
#per saperne di più guarda C:\Users\Samuele\Documents\Università\Python programs
    try:
        print('Inserisci i nomi dei file che vuoi plottare (premere INVIO per terminare):')
        source=[]
        while True:
            var=int(input())
            source.append(var)
            if var=='':
                break
    except ValueError:
        pass

def option(): #zoom di una particolare regione del grafico
    plt.figure()
    plt.xlabel('ciao come va')
    plt.ylabel('bella')
    plt.inset_axes([x0,y0,width,height])
    #plt.inset_axes(bounds=[x0,y0,width,height])
    # da qui in poi metti quello che vuoi
    x1, x2, y1, y2 = -1.5, -0.9, -2.5, -1.9
    axins.set_xlim(x1, x2)
    axins.set_ylim(y1, y2)
    axins.set_xticklabels([])
    axins.set_yticklabels([])
    ax.indicate_inset_zoom(axins, edgecolor="black")
    plt.show()


#program
OPTIONS = {
    0: option0,
    1: option1,
    2: option2,
    3: option3,
    4: option4,
    5: option5,
    6: option6,
    7: option7,
    8: option8,
    9: option9,
    10: option10,
    11: option11,
    12: option12,
    13: option13,
}

print("0 - calcolo area-baseline con plot ottimizzato (per prove)")
print("1 - calcolo area-baseline con plot ottimizzato + scrive su file")
print("2 - plot grafici variazione concentrazione + salvataggio immagine")
print("3 - plot grafici variazione flussi + salavataggio immagine")
print("4 - plot grafici variazione potenza + salavataggio immagine")
print("5 - plot grafici flussi 2:8 per potenze 40,90W + salvataggio immagine")
print("6 - plot grafici Concentrazione normalizzata vs flux/conc/power + salvataggio immagine")
print("7 - combinazione dei plot per conc/flux/power + salvataggio immagine")
print("8 - plot grafici Resa Energetica vs flux/conc/power + salvataggio immagine + scrive su file")
print("9 - combinazione dei plot per conc/flux/power + salvataggio immagine")
print("10 - plot grafici (statico)")
print("11 - plot grafici Resa Energetica vs time (statico)")
print("12 - plot grafici (confronto tubo basetta)(statico)")
print("13 - plot con zoom di una particolare regione del grafico")
print("\n")

while True:
    try:
        option=int(input("Quale opzione vuoi eseguire:"))
        if option in OPTIONS:
            OPTIONS[option]()
            break
        else:
            print("Errore: inserire un'opzione valida.")
    except ValueError:
        pass
