import subprocess

# Lanciare un .vbs e attendere la fine
subprocess.run(
	["cscript", "C:\\scripts\\job.vbs"],
	check=True
)
# 📌 Usa cscript (console) invece di wscript per evitare popup grafici.


# Lanciare un .vbs in background
subprocess.Popen(
	["cscript", "C:\\scripts\\job.vbs"]
)


# Passare parametri al .vbs
subprocess.run(
	["cscript", "job.vbs", "vendite.xlsx", "prod"]
)

# Catturare output e return code
result = subprocess.run(
	["cscript", "job.vbs"],
	capture_output=True,
	text=True
)

print("STDOUT:", result.stdout)		# se nel file lanciato c'è:		print("Calcolo completato")
print("STDERR:", result.stderr)		# se nel file lanciato c'è:		print("Attenzione: valore mancante", file=sys.stderr)
print("Exit code:", result.returncode)


'''
while True:
	result = subprocess.run(
		["cscript", vbs_file],
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