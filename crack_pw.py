import random as rd
import string as st

your_pw=input('Enter your password: ')
pw=list(your_pw)
guess,crack='',''
loading_symbols=['\\','|','/','-']
print('Cracking password')

for i in range(len(your_pw)):
    while guess != pw[i]:
        guess=rd.choice(st.ascii_letters+st.digits+st.punctuation)
        for symbol in loading_symbols:
            print(f"\r{symbol}",end='')
    crack=(''.join(crack+guess))
    
print('\nYour password is: ',crack)
