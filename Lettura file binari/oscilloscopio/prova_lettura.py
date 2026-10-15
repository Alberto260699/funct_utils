from read_bin import read_agilent_binary
import matplotlib.pyplot as plt
from pprint import pprint
from collections import Counter  # Per contare le occorrenze dei valori
import numpy as np  # Per operazioni numeriche
import os

var=str(input('Quale file vuoi caricare: '))
fl=var+'.bin'

#variabili
cwd=os.getcwd()

#load data
os.chdir(cwd+'/Dati')
data = read_agilent_binary(fl, include_time_vector=True)
pprint(data)

# Conta le occorrenze dei valori unici di y
value_counts = Counter(data['channel_1']['y_data'])

# Ordina i valori per ottenere un grafico chiaro
sorted_values = sorted(value_counts.items())  # Lista di tuple (valore, conteggio)
y_value, counts = zip(*sorted_values)  # Separazione in due liste: valori e conteggi

# Creazione del grafico
fig, ax1=plt.subplots()  # Primo asse
ax1.plot(data['channel_1']['x_data'], data['channel_1']['y_data'], label='Plot')

# Secondo asse
ax2 = ax1.twiny()  # Secondo asse x
ax2.plot(counts, y_value, color='orange', label='Media')

# Legende separate per ciascun asse
ax1.legend()
ax2.legend()

os.chdir(cwd+'/Immagini')
plt.savefig(var+'.png')
plt.show()