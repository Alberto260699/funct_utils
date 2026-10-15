import argparse
import logging
import sys
from pathlib import Path
import xlwings as xw

LOG_FILE = "quadratura.log"

def setup_logging():
	logging.basicConfig(
		filename=LOG_FILE,
		level=logging.INFO,
		format="%(asctime)s [%(levelname)s] %(message)s"
	)

def main():
	setup_logging()
	logging.info("Avvio script quadratura")
	
	parser = argparse.ArgumentParser(
		description="Elaborazione file Excel"
	)
	
	parser.add_argument('file', type=Path, help='File di quadratura')
	
	args = parser.parse_args()
	
	try:
		# Validazione file
		if not args.file.exists():
			logging.error("File non trovato: %s", args.file)
			sys.exit(1)
		
		# Esecuzione del file excel
		app = xw.App(visible=False)
		wb = app.books.open(str(args.file))
		#wb.save()
		wb.close()
		app.quit()
		
		logging.info(f'\nGenerazione del file {args.file} completata dei Documents')

if __name__ == '__main__':
	main()