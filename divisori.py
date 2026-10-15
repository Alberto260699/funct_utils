n=int(input('Inserisci il numero intero che vuoi: '))
primo=True
divisori=[1]
for i in range(2, n):
    if n%i==0:
        primo=False
        divisori.append(i)
divisori.append(n)
print('I divisori di', n, 'sono:')
print(divisori)
if primo:
    print(n, 'è un numero primo')
else:
    print(n, 'non è un numero primo')