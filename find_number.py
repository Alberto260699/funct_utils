import random as rm
n=rm.randint(1,10)
for i in range(0,5):    
    l=int(input('Inserisci il tuo numero tra 1 e 10: '))
    if(n==l):
        print('Hai indovinato complimennti!!!')
        break
    else:
        print('Ritenta sarai più fortunato')
