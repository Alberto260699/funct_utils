'''
LAVORARE TRA LE CARTELLE
'''
# copia l'intera cartella
shutil.copytree(os.path.join(plc_path, chius_prec), os.path.join(plc_path, var_chius))

# sposte e rinomina all'occorrenza
shutil.move(src, dst)

#copia
shutil.copy(src, dst)

#copia anche i metadati
shutil.copy2(src, dst)

# rinominare (se non esiste il file)
file = Path('report.xlsx')
file.rename('report_2025_09.xlsx')

# rinominare (se il file esiste già)
rename_file = {'old_name.txt': 'new_file.txt'}
for old_name, new_name in rename_file.items():
    src = base_dir / old_name
    dst = base_dir / new_name

    if src.is_file():
        src.replace(dst)
        logging.info("Rinominato %s → %s", src.name, dst.name)
    else:
        logging.warning("File non trovato: %s", src)

# eliminare (metodo 1)
from pathlib import Path
base = Path(chius_path)

for name in var_chius:
    file = base / name
    if file.is_file():
        file.unlink()
    else:
        logging.warning("File non trovato o non è un file: %s", file)

# con gestione degli errori
for name in var_chius:
    file = base / name
    try:
        file.unlink()
        logging.info("File eliminato: %s", file)
    except FileNotFoundError:
        logging.warning("File non trovato: %s", file)
    except PermissionError:
        logging.error("Permesso negato: %s", file)

# se var_chiu è una directory
dir_path = Path(chius_path) / var_chius

for file in dir_path.iterdir():
    if file.is_file():
        file.unlink()

#se var_chius è un pattern
for file in dir_path.glob('*.xlsx'):
    file.unlink()

	
# eliminare(metodo 2)
import os
if os.path.exists('file.txt'):
    os.remove('file.txt')
	
# lavroare con le directoy
from pathlib import Path
file = Path('documents/report.xlsx')

file.exists()     # True / False
file.is_file()    # True / False

file.name      # 'report.xlsx'
file.stem      # 'report'
file.suffix    # '.xlsx'