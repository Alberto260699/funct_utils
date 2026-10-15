import subprocess

# Percorso dello script
sh_file = "/home/user/script.sh"


# Lanciare un .sh e attendere la fine
result = subprocess.run(["/bin/bash", sh_file])
print("Return code:", result.returncode)


# Lanciare un .sh in background
process = subprocess.Popen(["/bin/bash", sh_file])
# Continua subito l’esecuzione del Python principale
print("Script lanciato in background")


# Passare parametri al .sh
subprocess.run(["/bin/bash", sh_file, "param1", "param2"])


# Catturare output e return code
result = subprocess.run(
    ["/bin/bash", sh_file],
    capture_output=True,
    text=True
)

print("STDOUT:", result.stdout)		# se nel file lanciato c'è:		print("Calcolo completato")
print("STDERR:", result.stderr)		# se nel file lanciato c'è:		print("Attenzione: valore mancante", file=sys.stderr)
print("Exit code:", result.returncode)



'''
while True:
	result = subprocess.run(
		["cscript", sh_file],
		capture_output=True,
		text=True
	)

	if result.returncode == 0:
		print("Script eseguito correttamente, continuo...")
		break
	else:
		print("Errore nello script, rilancio")
		print(result.stderr)
		continue
'''