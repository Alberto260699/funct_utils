import itertools				#per creare una sequenza infinita di caratteri
import threading			 	#per eseguire l'animazione in parallelo rispetto all'attività principale
import time
import sys
 
def animate_loading():
	for c in itertools.cycle(['|', '/', '-', '\\']):
		if stop_loading:
			break
		sys.stdout.write('\rCaricamento ' + c)		#scrive una riga direttamente sul terminale, riportatndo il cursore all'inzio
		sys.stdout.flush()
		time.sleep(0.1)
 
stop_loading = False
t = threading.Thread(target=animate_loading)
t.start() 

# Simula un'attività che richiede tempo
time.sleep(5) 

stop_loading = True
t.join()
print("\nCaricamento completato!")