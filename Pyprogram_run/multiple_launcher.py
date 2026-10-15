import subprocess
import sys

scripts = ["script2.py", "script3.py", "script4.py"]
processes = []

# Avvia tutti i processi senza aspettare
for s in scripts:
	p = subprocess.Popen([sys.executable, s])
	processes.append(p)

# Aspetta che tutti finiscano
for p in processes:
	p.wait()

print("Tutti gli script sono terminati")


'''
✅ Ogni script gira indipendentemente
✅ Buono per script “pesanti” o separati
'''

#--------------------------


from concurrent.futures import ProcessPoolExecutor
import subprocess
import sys

def run_script(script):
	return subprocess.run([sys.executable, script]).returncode

scripts = ["script2.py", "script3.py", "script4.py"]

with ProcessPoolExecutor() as executor:
	results = list(executor.map(run_script, scripts))

print("Return code di tutti gli script:", results)

'''
✅ Meno boilerplate
✅ Controllo più facile dei return code
✅ Adatto anche per calcoli CPU-bound
'''