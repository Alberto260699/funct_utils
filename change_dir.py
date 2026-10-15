import os #librearia per spostarti tra le cartelle

cwd=os.getcwd() #os.getcwd() permette di leggere il percorso file in cui sei 
print("Current working directory: "+format(cwd))
os.chdir(cwd+'/gc') #os.chdir(directory) permette di spostarti nella directory indiacata come oggetto
print("Current working directory: "+format(os.getcwd()))
os.chdir(cwd+'/Parametri') #ricorda che devi tornare indietro per cambiare il percorso
print("Current working directory: {0}".format(os.getcwd()))
#il print lo puoi scrivere nei due modi che desideri