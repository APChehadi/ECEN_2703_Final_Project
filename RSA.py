p = 0x10000000f
q = 0x10000003d
e = 0x10001
n = p*q
d = linearCongruence(e, 1, (p-1)*(q-1))

M = 0x4543454e32373033
print('M = ', hex(M))

C = mod_exponent(M, e, n)
print('C = ', hex(C))

P = mod_exponent(C, d, n)
print('P = ', hex(P))