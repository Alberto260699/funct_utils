class Persona:
	def __init__(self, nome, eta):
		self.nome = nome
		self.eta = eta

	def saluta(self):
		return f"Ciao, mi chiamo {self.nome} e ho {self.eta} anni."

# Esempio di utilizzo
p1 = Persona("Luca", 25)
print(p1.saluta())


# Esempio di ereditarietà
class Animale:
	def __init__(self, nome):
		self.nome = nome

	def parla(self):
		return "Suono generico"


class Cane(Animale):  # Eredita da Animale
	def parla(self):
		return "Bau!"


class Gatto(Animale):  # Eredita da Animale
	def parla(self):
		return "Miao!"


# Uso
cane = Cane("Fido")
gatto = Gatto("Micio")

print(f"{cane.nome} dice: {cane.parla()}")
print(f"{gatto.nome} dice: {gatto.parla()}")


# Esempio di proprietà
class Rettangolo:
	def __init__(self, base, altezza):
		self.base = base
		self.altezza = altezza

	@property
	def area(self):
		return self.base * self.altezza

	@property
	def perimetro(self):
		return 2 * (self.base + self.altezza)


# Uso
r = Rettangolo(5, 3)
print("Area:", r.area)		  # Non serve chiamare come funzione
print("Perimetro:", r.perimetro)
