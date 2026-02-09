import base64

def encrypt(x, n):
    key = 'qwertyuioplkjhgfdsazlfmhkb'

    if n == len(x):
        return ''.join(x)

    for i in range(n, len(x)):
        x[i] = chr(ord(x[i]) ^ ord(key[i - n]))

    return encrypt(x, n + 1)
def encrypt_flag(flag):
    return encrypt(list(flag), 0)

flag = "\"4Rj\x12(\\_^(,{\x00c\r,OS]e$j\x18,Dl"

enc_flag = encrypt_flag(flag)
print(repr(enc_flag))

# This script prints "\"4Rj\x12(\\_^(,{\x00c\r,OS]e$j\x18,Dl"
