#opzione 1
var='y'
fl=open('to-do list.txt', 'a')
while(var=='y'):
    var=input('Vuoi aggiungere qualcosa y/n?')
    if(var=='y'):
        fl.write('-'+input()+'\n')
    else:
        break
fl.close()
fl=open('to-do list.txt', 'r').read()
print(fl)

#opzione 2
var=int(input('Quante cose devi fare?'))
if(var!=0):
    fl=open('To-do-list.txt', 'a')
    for i in range(0,var):
        fl.write('-'+input()+'\n')
    fl.close()
lett=open('To-do-list.txt', 'r').read()
print(lett)

#se al posto di read metti readlines la lettura avviene come unica riga