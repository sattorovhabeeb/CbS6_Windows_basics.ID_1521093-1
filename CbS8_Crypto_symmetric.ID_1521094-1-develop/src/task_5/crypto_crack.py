import json
import random
import struct
import time
from base64 import b64encode
from Crypto.Cipher import ChaCha20
from Crypto.Random import get_random_bytes

random.seed(int(time.time()))
flag = b'???'
key = get_random_bytes(32)
nonce = struct.pack("<Q", random.randint(1, 2**64 - 1))
cipher = ChaCha20.new(key=key, nonce=nonce)
ciphertext = cipher.encrypt(flag)
result = json.dumps({'key': b64encode(key).decode('utf-8'), 'ciphertext': b64encode(ciphertext).decode('utf-8')})
print(result)


