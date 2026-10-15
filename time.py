import time as tm
t=tm.time()
print('Secondi passati: ', t)
local_t=tm.ctime()
print('Local time: ', local_t)
tm.sleep(3)
print('Scrive dopo 3 secondi')