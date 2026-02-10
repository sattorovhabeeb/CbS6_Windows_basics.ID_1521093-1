import codecs

# ОРИГИНАЛЬНЫЙ КОД С ОШИБКАМИ (для расшифровки)
def a(b):
    c, d, j = len(b), list(range(256)), 0
    for i in range(256):
        j = (j + d[i] + b[i % c]) % 255  # ОШИБКА 1: % 255
        d[i], d[j] = d[j], d[i]
    return d


def b(c):
    i, j = 0, 0
    while True:
        i = (i + 1) % 256
        j = (j + c[i]) % 256
        c[i], c[j] = c[j], c[i]
        k = c[(c[i] + c[i]) % 256]  # ОШИБКА 2: c[i] + c[i]
        yield k

def c(k):
    x = a(k)
    return b(x)

def d(k, t):
    k = [ord(u) for u in k]
    f = c(k)
    o = []
    for u in t:
        v = u ^ next(f)
        o.append(v)
    return bytes(o)


# Функция для расшифровки
def decrypt(key_str, ciphertext_hex):
    """Расшифровка используя оригинальный баганый код"""
    key = [ord(u) for u in key_str]
    ciphertext_bytes = bytes.fromhex(ciphertext_hex)
    
    keystream = c(key)
    plaintext = []
    for byte in ciphertext_bytes:
        plaintext.append(byte ^ next(keystream))
    
    return bytes(plaintext)


def main():
    key = 'Za1EDolzhrRdPAehiGHu82HXkPa92zpd1Ofg'
    ciphertext_hex = '3F7307755A4336416DA27ED3CE1DE715387285E84CE3130EC0CD8F748CAA'
    
    print("=== РАСШИФРОВКА ОРИГИНАЛЬНЫМ (БАГАНЫМ) КОДОМ ===")
    print(f"Ключ: {key}")
    print(f"Шифртекст: {ciphertext_hex}")
    print()
    
    # Расшифровываем
    plaintext_bytes = decrypt(key, ciphertext_hex)
    
    # Пробуем разные кодировки
    print("Попытка декодирования:")
    try:
        plaintext = plaintext_bytes.decode('utf-8')
        print(f"UTF-8: {plaintext}")
    except:
        print("UTF-8: не удалось")
    
    try:
        plaintext = plaintext_bytes.decode('latin-1')
        print(f"Latin-1: {plaintext}")
    except:
        print("Latin-1: не удалось")
    
    print(f"\nБайты (hex): {plaintext_bytes.hex()}")
    print(f"Байты (raw): {plaintext_bytes}")
    
    # Проверка обратным шифрованием
    print("\n=== ПРОВЕРКА ===")
    key_bytes = [ord(u) for u in key]
    keystream2 = c(key_bytes)
    encrypted_back = []
    for byte in plaintext_bytes:
        encrypted_back.append(byte ^ next(keystream2))
    
    encrypted_hex = bytes(encrypted_back).hex().upper()
    print(f"Зашифровано обратно: {encrypted_hex}")
    
    if encrypted_hex == ciphertext_hex.upper():
        print("✓ ПРОВЕРКА ПРОЙДЕНА!")
        print(f"\n{'='*60}")
        print(f"ФЛАГ: {plaintext}")
        print(f"{'='*60}")
    else:
        print("✗ Проверка не прошла")
        print("\nРазница:")
        print(f"Ожидалось: {ciphertext_hex.upper()}")
        print(f"Получено:  {encrypted_hex}")


if __name__ == "__main__":
    main()
