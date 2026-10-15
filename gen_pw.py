import random as rd
import string as st
import time as tm

lenght=int(input('Quanto deve essere lungha la PW: '))
print(''.join(rd.choice(st.ascii_letters+st.digits+st.punctuation) for i in range(lenght)))
#join prende tutti gli item e li unisce in una unica stringa
tm.sleep(10)



import secrets
import string

caratteri = string.ascii_letters + string.digits + "!@#$%&"

password = ''.join(
    secrets.choice(caratteri)
    for _ in range(16)
)

print(password)



import secrets

token = secrets.token_hex(16)
numero = secrets.randbits(8)
numero = secrets.randbits(16)
numero = secrets.randbelow(100)

print(token)