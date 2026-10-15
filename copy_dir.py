import shutil

origine = "percorso/cartella_origine"
destinazione = "percorso/cartella_destinazione"

# Se la cartella di destinazione non esiste
shutil.copytree(origine, destinazione)

# Se la cartella di destinazione esiste
shutil.copytree("origine", "destinazione", dirs_exist_ok=True)


#----------------------------

# Copia solo i file senza sottocartelle
import os
import shutil

origine = "origine"
destinazione = "destinazione"

os.makedirs(destinazione, exist_ok=True)

for file in os.listdir(origine):
	src = os.path.join(origine, file)
	dst = os.path.join(destinazione, file)
	if os.path.isfile(src):
		shutil.copy2(src, dst)
		
#------------------------------

# Gestione degli errori
try:
	shutil.copytree("origine", "destinazione")
except FileExistsError:
	print("La cartella di destinazione esiste già")
except Exception as e:
	print("Errore:", e)
	
#------------------------------

# Test minimo di sicurezza
import shutil
from pathlib import Path

src = Path("origine")
dst = Path("destinazione")

if src.exists() and src.is_dir():
	shutil.copytree(src, dst, dirs_exist_ok=True)
else:
	print("Cartella sorgente non valida")
