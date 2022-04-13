from random import randrange, getrandbits
from math import gcd
import hashlib


def is_prime(num):
    if num == 2:
        return True
    if num < 2 or num % 2 == 0:
        return False
    for n in range(3, int(num**0.5)+2, 2):
        if num % n == 0:
            return False
    return True


def prime_generator():
    notprime = True
    while notprime:
        num = randrange(0, getrandbits(8))
        if is_prime(num):
            return num


def publickey_generator(phi):
    notfound = True
    while notfound:
        e = randrange(0, getrandbits(8))
        res = gcd(e, phi)
        if res == 1:
            return e


def privatekey_generator(e, phi):
    if e == 0:
        return (0, 1)
    else:
        y, x = privatekey_generator(phi % e, e)
        return (x - (phi // e) * y, y)


def file_read(file_name):
    res = open(file_name)
    return (res.read())


def initialize():
    p = prime_generator()
    q = prime_generator()
    n = p * q
    phi = (p-1) * (q-1)
    e = publickey_generator(phi)
    d = privatekey_generator(e, phi)

    d = d[0] % phi
    if(d < 0):
        d += phi

    print("p =", p)
    print("q =", q)
    print("n =", n)
    print("phi =", phi)

    txtprivate = open('private.pri', 'w')
    txtprivate.write(str(d))
    txtprivate.close()

    txtpublic = open('public.pub', 'w')
    txtpublic.write(str(e))
    txtpublic.close()

    return(n)


def digest(text):
    res = hashlib.sha1(text.encode())
    return res.hexdigest()


def sign(file_name, message_digest):
    with open(file_name, "a+") as file_object:
        file_object.seek(0)
        text = file_object.read(100)
        if len(text) > 0:
            file_object.write("\n")
        file_object.write("<ds>" + message_digest + "</ds>")


def to_ascii(list):
    result = []
    for letter in list:
        result.append(ord(letter) - ord('a'))
    return result


def to_hex(list):
    result = []
    for number in list:
        result.append((hex(number)).replace('0x', ''))
    return ''.join(result)


def encrypt(plaintext, key, n):
    plaintext_ascii = to_ascii(plaintext)

    result = []
    for number in plaintext_ascii:
        result.append((number ** int(key)) % n)

    ciphertext = to_hex(result)
    return(ciphertext)


n = initialize()

pub = file_read("public.pub")
print(pub)

pri = file_read("private.pri")
print(pri)

doc = file_read("document.txt")
message_digest = digest(doc)
encrypted_message_digest = encrypt(message_digest, pri, n)
sign("document.txt", encrypted_message_digest)
