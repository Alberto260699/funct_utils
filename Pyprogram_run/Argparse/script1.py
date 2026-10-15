import subprocess
import sys
from datetime import date

file_excel = "vendite.xlsx"
data = date.today().isoformat()
modo = "prod"

print("Avvio script2...")

result = subprocess.run(
	[
		sys.executable,
		"script2.py",
		"--file", file_excel,
		"--data", data,
		"--modo", modo
	],
	check=False,			# non solleva eccezione se returncode != 0
	capture_output=True,	# cattura stdout e stderr
	text=True				# decodifica l’output come stringa (non byte)
)

# Gestione return code
if result.returncode == 0:
	print("SUCCESSO: script2 completato")
elif result.returncode == 1:
	print("ERRORE PARAMETRI")
elif result.returncode == 2:
	print("FILE NON TROVATO")
elif result.returncode == 3:
	print("ERRORE ELABORAZIONE")
else:
	print(f"ERRORE IMPREVISTO (code={result.returncode})")