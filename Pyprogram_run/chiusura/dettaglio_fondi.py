import argparse
import logging
import sys
from pathlib import Path
import xlwings as xw

LOG_FILE = "dettaglio_fondi.log"

def setup_logging():
	logging.basicConfig(
		filename=LOG_FILE,
		level=logging.INFO,
		format="%(asctime)s [%(levelname)s] %(message)s"
	)

def main():
	setup_logging()
	logging.info("Avvio report di dettaglio fondi")
	
	parser = argparse.ArgumentParser(
		description="Elaborazione file Excel"
	)
	
	parser.add_argument('file', type=Path, help='Report dettaglio fondi')
	
	args = parser.parse_args()
	
	try:
		# Validazione file
		if not args.file.exists():
			logging.error("File non trovato: %s", args.file)
			sys.exit(1)
		
		# Esecuzione del file 
		app = xw.App(visible=True)
		wb = app.books.open(str(args.file))
		#wb.save()
		wb.close()
		app.quit()
		
		logging.info(f'\nGenerazione del file {args.file} completata nella directory: ' + Path('da Riccardo' / 'dati per chiusura'))

if __name__ == '__main__':
	main()