import numpy as np

data=np.genfromtxt('Voltage_10V.txt', delimiter=',')
media=np.mean(data[:,1])
dev=np.std(data[:,1])
print(media)
print(dev)