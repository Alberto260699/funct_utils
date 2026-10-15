import sys

# Controllo parametri
if len(sys.argv) != 4:
	print("Uso: script2.py <file_excel> <data> <modalita>")
	sys.exit(1)

file_excel = sys.argv[1]
data = sys.argv[2]
modalita = sys.argv[3]

print("Parametri ricevuti:")
print(f"File Excel : {file_excel}")
print(f"Data	   : {data}")
print(f"Modalità   : {modalita}")

# Simulazione elaborazione
if modalita == "debug":
	print("Modalità DEBUG: nessuna scrittura su file")
else:
	print(f"Elaborazione del file {file_excel} in corso...")
