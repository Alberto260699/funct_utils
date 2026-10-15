import argparse
import logging
import sys
from datetime import datetime
from pathlib import Path

LOG_FILE = "script2.log"

'''
Salvi solo sul file di log e non sulla console, in questo modo nel chiamante non puoi utilizzare stdout/stderr
'''
def setup_logging():
	logging.basicConfig(
		filename=LOG_FILE,
		level=logging.INFO, #se vuoi fare DEBUG allora diventa level=logging.DEBUG
		format="%(asctime)s [%(levelname)s] %(message)s"
	)
	
'''
In questo caso salvi FILE + CONSOLE, quindi nel chiamante puoi utilizzare stdout/stderr se fai la cattura

def setup_logging():
	logging.basicConfig(
		level=logging.INFO,
		format="%(asctime)s [%(levelname)s] %(message)s",
		handlers=[
			logging.FileHandler(LOG_FILE),
			logging.StreamHandler()
		]
	)
'''

def main():
	setup_logging()
	logging.info("Avvio script2")

	parser = argparse.ArgumentParser(
		description="Elaborazione file Excel"
	)

	parser.add_argument("--file", required=True)
	parser.add_argument("--data", required=True)
	parser.add_argument(
		"--modo",
		choices=["debug", "prod"],
		default="prod"
	)

	try:
		args = parser.parse_args()

		# Validazione file
		file_path = Path(args.file)
		if not file_path.exists():
			logging.error("File non trovato: %s", args.file)
			sys.exit(2)

		# Validazione data
		try:
			data = datetime.strptime(args.data, "%Y-%m-%d").date()
		except ValueError:
			logging.error("Formato data non valido: %s", args.data)
			sys.exit(1)

		logging.info("Parametri OK - File=%s Data=%s Modo=%s",
					 file_path, data, args.modo)

		# Elaborazione simulata
		if args.modo == "debug":
			logging.info("Modalità DEBUG: nessuna modifica")
		else:
			logging.info("Elaborazione file in corso...")
			# >>> qui va la logica vera <<<
			logging.info("Avvio elaborazione report")
			
			if not file.exists():
				logging.error("File report mancante")
				sys.exit(1)
				
			if not file.exists():
				logging.critical("File report mancante")
				sys.exit(2)
			
			if files_extra:
				logging.warning("File extra trovati, verranno ignorati")
			
			logging.debug(f"Record letti: {len(records)}")
			logging.debug(f"Valore x={x}")
			logging.debug(f"File letti: {len(files)}")
			logging.debug(f"Parametri CLI: {args}")
			
			logging.info("Elaborazione completata con successo")
			
			
			# Log degli errori automatici (try/except)
			try:
				1 / 0
			except Exception:
				logging.exception("Errore critico")

'''
Livello		Quando usarlo
DEBUG		Dettagli tecnici
INFO		Eventi normali
WARNING		Situazioni anomale
ERROR		Errori gestiti
CRITICAL	Blocco totale
'''