import subprocess
import sys
from datetime import date

# Parametri da passare
file_excel = "vendite.xlsx"
data_elaborazione = date.today().isoformat()
modalita = "prod"   # oppure "debug"

print("Avvio script2...")

subprocess.run(
	[
		sys.executable,   # stesso Python
		"script2.py",
		file_excel,
		data_elaborazione,
		modalita
	],
	check=True
)

print("script2 terminato correttamente")
