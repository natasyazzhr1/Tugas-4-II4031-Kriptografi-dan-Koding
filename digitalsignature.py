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


def file_read_lines(file_name):
    with open(file_name, 'r') as f:
        text = f.readlines()
    return str(text)


def file_read(file_name):
    doc = open(file_name)
    return doc.read()


def initialize(p, q):
    # p = prime_generator()
    # q = prime_generator()
    n = p * q
    phi = (p-1) * (q-1)
    e = publickey_generator(phi)
    d = privatekey_generator(e, phi)

    d = d[0] % phi
    if(d < 0):
        d += phi

    # print("p =", p)
    # print("q =", q)
    # print("n =", n)
    # print("phi =", phi)

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


def set_sign(file_name, message_digest):
    with open(file_name, "a") as f:
        f.write("\n" + "<ds>" + message_digest + "</ds>")
    return f


def to_ascii(list):
    result = []
    for letter in list:
        result.append(ord(letter))
    return result


def to_dec(list):
    result = int(list, 16)
    return result


def to_hex(list):
    result = hex(list).replace('0x', '')
    return result


def to_string(list):
    result = []
    for number in list:
        result.append(chr(number))
    return ''.join(result)


def encrypt(plaintext, key, n):
    result = plaintext ** int(key) % n
    return(result)


def decrypt(ciphertext, key, n):
    result = ciphertext ** int(key) % n
    return(result)


def get_sign(file_name):
    with open(file_name, 'r') as f:
        message_digest = f.readlines()[-1]
        if "<ds>" and "</ds>" in message_digest:
            message_digest = message_digest.replace("<ds>", "")
            message_digest = message_digest.replace("</ds>", "")
        else:
            message_digest = "0"
    return message_digest


def get_message(file_name):
    message_file_name = "message.txt"
    sign_file_name = "signature.txt"
    with open(file_name, 'r') as f, open(message_file_name, 'w') as f2, open(sign_file_name, 'w') as f3:
        fcontent = f.readlines()
        fcontent = fcontent[:len(fcontent)-1]
        lastcontent = fcontent[len(fcontent)-1]
        lastcontent = lastcontent[:len(lastcontent)-1]
        fcontent[len(fcontent)-1] = lastcontent
        f2.writelines(fcontent)


def authenticate(message_digest1, message_digest2):
    return message_digest1 == message_digest2


def authenticate():
    authenticity = verify(decrypted_message_digest, result_received_md)
    print(authenticity)
    if authenticity == true:
        return "verified"
    else:
        return "there has been some changes"


def sign(file_name, pri_name, n):
    pri = file_read(pri_name)
    doc = file_read(file_name)
    hashed_sent_md = digest(doc)
    dec_hashed_sent_md = to_dec(hashed_sent_md)
    encrypted_message_digest = encrypt(dec_hashed_sent_md, pri, n)
    set_sign(file_name, str(to_hex(encrypted_message_digest)))


def verify(file_name, pub_name, n):
    pub = file_read(pub_name)
    message_digest = get_sign(file_name)
    decrypted_message_digest = decrypt(to_dec(message_digest), pub, n)
    get_message(file_name)
    message = file_read("message.txt")
    hashed_received_md = digest(message)
    result_received_md = to_dec(hashed_received_md) % n

    if result_received_md == decrypted_message_digest:
        return "verified"
    else:
        return "there has been some changes"
