import os
import filecmp

def confronta_file(file1, file2):
	'''Confronta due file singoli byte per byte.'''
	print(f'\n📄 Confronto diretto tra:\n  {file1}\n  {file2}')
	try:
		uguali = filecmp.cmp(file1, file2, shallow=False)
		if uguali:
			print('I file sono identici.')
		else:
			print('I file sono diversi.')
	except FileNotFoundError as e:
		print(f'Errore: {e}')

def confronta_lista_file(cartella1, cartella2):
	'''Confronta i file comuni in due directory (non ricorsivo).'''
	print(f'\nConfronto file comuni tra:\n  {cartella1}\n  {cartella2}')

	files1 = set(os.listdir(cartella1))
	files2 = set(os.listdir(cartella2))

	comuni = list(files1 & files2)
	if not comuni:
		print('Nessun file con lo stesso nome trovato.')
		return

	uguali, diversi, errori = filecmp.cmpfiles(cartella1, cartella2, comuni, shallow=False)

	if uguali:
		print('\nFile identici:')
		for f in uguali:
			print(f'  {f}')

	if diversi:
		print('\nFile diversi:')
		for f in diversi:
			print(f'  {f}')

	if errori:
		print('\nFile non confrontabili:')
		for f in errori:
			print(f'  {f}')

def confronta_cartelle(cartella1, cartella2):
	'''Confronta due directory in modo ricorsivo.'''
	print(f'\nConfronto ricorsivo tra:\n  {cartella1}\n  {cartella2}')
	confronto = filecmp.dircmp(cartella1, cartella2)
	mostra_risultati(confronto)

def mostra_risultati(confronto):
	'''Stampa i risultati del confronto tra directory.'''
	if confronto.left_only:
		print('\nSolo nella prima cartella:')
		for elemento in confronto.left_only:
			print(f'  {elemento}')

	if confronto.right_only:
		print('\nSolo nella seconda cartella:')
		for elemento in confronto.right_only:
			print(f'  {elemento}')

	if confronto.diff_files:
		print('\nFile con lo stesso nome ma contenuto diverso:')
		for elemento in confronto.diff_files:
			print(f'  {elemento}')

	if confronto.common_files and not confronto.diff_files:
		print('\nFile comuni identici trovati.')

	# Ricorsione su sottocartelle comuni
	for sotto in confronto.subdirs:
		print(f'\nConfronto sottocartella comune: {sotto}')
		mostra_risultati(confronto.subdirs[sotto])

if __name__ == '__main__':
	print('=== Programma di confronto file e cartelle ===')
	print('1 - Confronto di due file')
	print('2️ - Confronto di file comuni in due cartelle')
	print('3️ - Confronto completo di due cartelle (ricorsivo)')
	
	scelta = input('\nScegli il tipo di confronto (1, 2 o 3): ').strip()

	if scelta == '1':
		f1 = input('Percorso del primo file: ').strip()
		f2 = input('Percorso del secondo file: ').strip()
		confronta_file(f1, f2)

	elif scelta == '2':
		d1 = input('Percorso della prima cartella: ').strip()
		d2 = input('Percorso della seconda cartella: ').strip()
		confronta_lista_file(d1, d2)

	elif scelta == '3':
		d1 = input('Percorso della prima cartella: ').strip()
		d2 = input('Percorso della seconda cartella: ').strip()
		confronta_cartelle(d1, d2)

	else:
		print('❌ Scelta non valida.')
