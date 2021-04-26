import sympy
import math
import random
from cryptography.fernet import Fernet

# Steps of Hybrid RSA
"""
    1. Generate a symmetric key. The symmetric key needs to be kept a secret.
    2. Encrypt the data using the secret symmetric key.
    3. The person to whom we wish to send a message will share public key and keep the private key a secret.
    4. Encrypt the symmetric key using the public key of the receiver.
    5. Send the encrypted symmetric key to the receiver.
    6. Send the encrypted message text.
    7. The receiver decrypts the encrypted symmetric key using private key and gets the symmetric key needed for decryption.
    8. The receiver uses the decrypted symmetric key to decrypt the message, getting the original message.
"""



"""
    Functions
"""
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

# Computes the cyphertext C value by modular exponentiation
def encrypt_decrypt_message(char_val, enc_dec_bool, n, e, d):
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
            print('No modular inverse for ' + str(char_val))
        return M

# Copmute numeric value of each string character, and encrypt each character
# with the encrypt_decrypt_message function
def numeric_string_conversion(message, enc_dec_bool, n, e, d):
    return(''.join([chr(encrypt_decrypt_message(ord(char), enc_dec_bool, n, e, d)) for char in list(message)]))


"""
    1. Generate a symmetric key. The symmetric key needs to be kept a secret.
"""
# Generate secret key using Fernet
secret_symmetric_key = Fernet.generate_key()
print('Secret Key:', secret_symmetric_key)

# Instatiate the Fernet class with the secret key
fernet = Fernet(secret_symmetric_key)



"""
    2. Encrypt the data using the secret symmetric key.
"""
# User input (Alice), message to encrypt
input_message = input("\nEnter Message: ")

# Genereate encrypted message from fernet library and secret key
encrypted_message = fernet.encrypt(input_message.encode())
print("Alice Encrypted Message: ", encrypted_message)



"""
    3. The person to whom we wish to send a message will share public key and keep the private key a secret.
"""
# Generate 2 large prime values between 1 - 1000
Bob_p = sympy.randprime(1, 1000)
Bob_q = sympy.randprime(1, 1000)

# n value
Bob_n = Bob_p*Bob_q

# Euler's totient function
Bob_phi_n = (Bob_p-1)*(Bob_q-1)

# Generate value of e, ensure it is coprime with phi_n
Bob_e = 0
while(math.gcd(Bob_e, Bob_phi_n) != 1):
    Bob_e = sympy.randprime(1, 1000)

Bob_d = inverse_mod(Bob_e, Bob_phi_n)

# Bob's Public Key
print('\nBob Public Key (n, e):', (Bob_n, Bob_e))

# Bob's Private Key
print('Bob Private Key (n, d):', (Bob_n, Bob_d))



"""
    4. Encrypt the symmetric key using the public key of the receiver.
"""
# Sender: Alice
# Receiver: Bob
encrypted_secret_key = numeric_string_conversion(str(secret_symmetric_key), True, Bob_n, Bob_e, 0)
print('\nAlice Encrypted Secret Key:', encrypted_secret_key)



"""
    5. Send the encrypted symmetric key to the receiver.
    6. Send the encrypted message text.
"""
# The encrypted symmetric key (encrypted_secret_key) and the encrypted message (encrypted_message) are both globally 
# scoped in this python file, so Bob/receiver have access to them



"""
    7. The receiver decrypts the encrypted symmetric key using private key and gets the symmetric key needed for decryption.
"""
# Decrypting the secret key using Bob's private key. The secret key will be utilized to decrypt the message.
print('\nDecrypting Secret Key...')
dencrypted_secret_key = numeric_string_conversion(encrypted_secret_key, False, Bob_n, 0, Bob_d)
print('Bob Decrypted Secret Key:', dencrypted_secret_key)



"""
    8. The receiver uses the decrypted symmetric key to decrypt the message, getting the original message.
"""
# Decrypting message with the fernat instance of the secret key that was used for encrypting the string
print('\nDecrypting Message...')
decrypted_message = fernet.decrypt(encrypted_message).decode()
print('Bob Decrypted Message:', decrypted_message)