from pathlib import Path
import argparse
import logging
import sys
import json

LOG_FILE = 'rinomina-eliminazione.log'

def setup_logging():
	logging.basicConfig(
		filename=LOG_FILE,
		level=logging.INFO,
		format='%(asctime)s [%(levelname)s] %(message)s'
	)

def main():
	setup_logging()
	logging.info("Avvio rinomina/eliminazione dei file indicati")
	
	parser = argparse.ArgumentParser(
		description='Rinomina o eliminazione dei file'
	)
	
	parser.add_argument('--mode', choices=['delete', 'rename'], default='delete',
						help='Modalità: 'delete' (cancellazione file) o 'rename' (rinomina file)')
	parser.add_argument('file', type=json.loads, help='Lista file')
	parser.add_argument('--path', type=Path, default=None, help='Path di lavoro')

	args = parser.parse_args()
	
	if args.mode == 'delete':
		logging.info('Modalità ELIMINAZIONE')
		for name in args.file:
			file_tmp = args.path / name
			if file_tmp.is_file():
				try:
					file_tmp.unlink()
					logging.info(f"File eliminato: {file_tmp}")
				except PermissionError:
					logging.warning(f"Permesso negato: {file_tmp}")
				except Exception as e:
					logging.warning(f"Errore eliminando {file_tmp}: {e}")
			else:
				logging.error(f"File non trovato o non è un file: {file_tmp}")
		
		logging.info(f'\nCancellazione dei file {args.path}')
		
	elif args.mode == 'rename':
		logging.info('Modalità RINOMINA')
		
		new_name = name(args.path)				# name restituiesce sempre e solo l'ultima radice del path
		#new_name = parts(args.path)[-1]		# part invece prende la radice che più preferisci
		#new_name = old_name.replace("202601", "202602")
		
		for old_name in args.file.items():
			src = args.path / old_name
			dst = args.path / new_name

			if src.is_file():
				src.replace(dst)
				logging.info("Rinominato %s → %s", src.name, dst.name)
			else:
				logging.warning("File non trovato: %s", src)

if __name__ == '__main__':
	main()