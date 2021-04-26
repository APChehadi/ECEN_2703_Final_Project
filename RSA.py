import sympy
import math
import random



"""
    Bob's Private and Public Key Generation
"""

# Generate 2 large prime values between 1 - 1000
p = sympy.randprime(1, 1000)
q = sympy.randprime(1, 1000)
print('p = ', p)
print('q = ', q)

# n value
n = p*q
print('n = ', n)

# Euler's totient function
phi_n = (p-1)*(q-1)
print('phi_n = ', phi_n)

# Generate value of e, ensure it is coprime with phi_n
e = 0
while(math.gcd(e, phi_n) != 1):
    e = sympy.randprime(1, 1000)
print('e = ', e)

# Generate d value, the inverse of e modulo phi_n
# Recursive extended gcd implementation
def extended_gcd(a, b):
    if(a == 0):
        return(b, 0, 1)
    else:
        g, y, x = extended_gcd(b % a, a)
        return(g, x - (b//a) * y, y)

# Modulo inverse function implementation
def inverse_mod(a, m):
    g, x, y = extended_gcd(a, m)
    if(g != 1):
        raise Exception('No modular inverse')
    return(x % m)

d = inverse_mod(e, phi_n)
print('d =', d)

# Bob's Public Key
print('Bob Public Key (n, e): ', (n,e))

# Bob's Private Key
print('Bob Private Key (n, d): ', (n,d))



"""
    Alice enters plaintext message, and encrypts message
"""
input_message = input("\nEnter message: ")

# Computes the cyphertext C value by modular exponentiation
def encrypt_decrypt_message(char_val, enc_dec_bool):
    # True => Encrypt
    if enc_dec_bool:
        C = inverse_mod(char_val**e, n)
        if C == None:
            print('No modular inverse for ' + str(char_val))
        return C
    # False => Decrypt
    else:
        M = inverse_mod(char_val**d, n)
        if M == None:
            print('No modular inverse for ' + str(cyphertext_C))
        return M

# Copmute numeric value of each string character, and encrypt each character
# with the encrypt_decrypt_message function
def numeric_string_conversion(message, enc_dec_bool):
    return(''.join([chr(encrypt_decrypt_message(ord(char), enc_dec_bool)) for char in list(message)]))

cyphertext_C = numeric_string_conversion(input_message, True)
print('Alice Encrypted message / cyphertext C: ', cyphertext_C)

plaintext_M = numeric_string_conversion(cyphertext_C, False)
print('Bob Decrypted message / plaintext_M: ', plaintext_M)

