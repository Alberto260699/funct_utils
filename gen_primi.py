import numpy as np
import random as rd
import time as tm

t=tm.time()
num=0
primo=True
primi=[]
while num<t:
    for i in range(1,num):
        if num%i==0:
            primo=False
    if primo==True:
        primi.append(num)
    t=t+tm.time()
    num=num+1
print(primi)