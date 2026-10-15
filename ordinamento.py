# =========================
# ORDINAMENTO
# =========================

v = [5,2,7,1,8,3,6,4]

# =========================
# 1
# =========================

def qs(v):
	if len(v) <= 1:
		return v
	p,L,R = v[0], [], []
	for x in v[1]:
		if x < p:
			L.append(x)
		else:
			R.append(x)
	return qs(L) + [p] + qs(R)

print(qs(v))

# =========================
# 2
# =========================

n = len(v)
for i in range(n-1):
	ok = True
	for j in range(n-1-i):
		if v[j] > v[j+1]:
			v[j], v[j+1] = v[j+1], v[j]
			ok = False
	if ok:
		break

print(v)

# =========================
# PALIDORMA
# =========================

def is_palindrome(string):
	return string ==  string[:: -1] #scorre da inizio alla fine in ordine inverso
	
print(is_palindrome('madam'))

def max_area(height):
	l,r = 0, len(height)-1
	best = 0
	while l < r:
		h = min(height[l], height[r])
		if h*(r-l) > best:
			best = h*(r-l)
		if height[l] < height[r]:
			l += 1
		else:
			r -= 1
	return best