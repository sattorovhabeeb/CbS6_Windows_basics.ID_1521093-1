import os
from Crypto.Cipher import AES

def xor(one, two):
    return bytes(a ^ b for (a, b) in zip(one, two))

plaintext = "???"
key = b'Super_Secret_' + os.urandom(3)
iv = os.urandom(16)

cbc = AES.new(key, AES.MODE_CBC, iv)
ct1 = cbc.encrypt(plaintext)
print(ct1.hex())
