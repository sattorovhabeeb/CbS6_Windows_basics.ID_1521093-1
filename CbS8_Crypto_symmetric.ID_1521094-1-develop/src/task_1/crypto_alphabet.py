import os
from Crypto.Cipher import DES
import string

def super_encryption(plaintext, key):
    ct = b''
    cipher = DES.new(key, DES.MODE_ECB)
    for a_letter in plaintext:
        ct += cipher.encrypt((a_letter * 8).encode())
    return ct

key = os.urandom(8)
flag = "S21{are_you_sure_about_this_algo?}"

ciphertext1 = super_encryption(string.printable, key)
ciphertext2 = super_encryption(flag, key)

print(ciphertext1.hex())
print(ciphertext2.hex())
