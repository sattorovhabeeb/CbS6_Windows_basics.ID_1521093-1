import codecs

def a(b):
    c, d, j = len(b), list(range(256)), 0
    for i in range(256):
        j = (j + d[i] + b[i % c]) % 255
        d[i], d[j] = d[j], d[i]
    return d


def b(c):
    i, j = 0, 0
    while True:
        i = (i + 1) % 256
        j = (j + c[i]) % 256
        c[i], c[j] = c[j], c[i]
        k = c[(c[i] + c[i]) % 256]
        yield k

def c(k):
    x = a(k)
    return b(x)

def d(k, t):
    k = [ord(u) for u in k]
    f = c(k)
    o = []
    for u in t:
        v = ("%02X" % (u ^ next(f)))
        o.append(v)
    return ''.join(o)


def e(k, p):
    p = [ord(c) for c in p]
    return d(k, p)

def main():
    a = 'Za1EDolzhrRdPAehiGHu82HXkPa92zpd1Ofg'
    b = '???'
    c = e(a, b)
    print("Ciphertext:", c)

    if c == '3F7307755A4336416DA27ED3CE1DE715387285E84CE3130EC0CD8F748CAA':
        print("Correct test!")
    else:
        print("Wrong test!")

if __name__ == "__main__":
    main()
