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
    # result = []
    # for number in list:
    #     result.append(int(number,16))
    result = int(list, 16)
    return result


def to_hex(list):
    # result = []
    # for number in list:
    #     result.append((hex(number)).replace('0x', ''))
    result = hex(list).replace('0x', '')
    return result


def to_string(list):
    result = []
    for number in list:
        result.append(chr(number))
    return ''.join(result)


def encrypt(plaintext, key, n):
    # plaintext_ascii = to_ascii(plaintext)
    # print(plaintext_ascii)

    # result = []
    # for number in plaintext_ascii:
    #     result.append((number ** int(key)) % n)
    result = plaintext ** int(key) % n
    # print('result',result)

    # ciphertext = []
    # ciphertext = to_hex(result)

    return(result)


def decrypt(ciphertext, key, n):
    # ciphertext_dec = to_dec(ciphertext) #diubah ke decimal
    # print('result',ciphertext_dec)

    # result = []
    # for number in ciphertext_dec:
    #     result.append((number ** int(key)) % n)
    # print(result)
    result = ciphertext ** int(key) % n
    # print('result', result)

    # plaintext = to_string(result)
    return(result)


def get_sign(file_name):
    with open(file_name, 'r') as f:
        message_digest = f.readlines()[-1]
        message_digest = message_digest.replace("<ds>", "")
        message_digest = message_digest.replace("</ds>", "")
    return message_digest


def get_message(file_name):
    message_file_name = "message.txt"
    sign_file_name = "signature.txt"
    with open(file_name, 'r') as f, open(message_file_name, 'w') as f2, open(sign_file_name, 'w') as f3:
        fcontent = f.readlines()
        fcontent = fcontent[:len(fcontent)-1]
        lastcontent = fcontent[len(fcontent)-1]  # ini string terakhir
        lastcontent = lastcontent[:len(lastcontent)-1]  # hapus new line
        fcontent[len(fcontent)-1] = lastcontent  # assign balik ke last element
        f2.writelines(fcontent)


def verify(message_digest1, message_digest2):
    return message_digest1 == message_digest2


def authenticate():
    authenticity = verify(decrypted_message_digest, result_received_md)
    print(authenticity)
    if authenticity == true:
        return "verified"
    else:
        return "there has been some changes"


def sign(file_name, pri_name, pub_name, n):
    pub = file_read(pri_name)
    print('public key', pub)

    pri = file_read(pub_name)
    print('private key', pri)

    doc = file_read(file_name)
    # print('awal', doc)

    hashed_sent_md = digest(doc)
    print('fungsi hash', hashed_sent_md)

    dec_hashed_sent_md = to_dec(hashed_sent_md)
    # print('decimal', dec_hashed_sent_md)

    encrypted_message_digest = encrypt(dec_hashed_sent_md, pri, n)
    print('fungsi encrypt', encrypted_message_digest)

    # encrypted_message_digest = encrypt(hashed_sent_md, pri, n)
    # print_encrypted_message_digest = ''.join(encrypted_message_digest)
    # print('fungsi encrypt', print_encrypted_message_digest)

    set_sign(file_name, str(to_hex(encrypted_message_digest)))


# message_digest = get_sign(file_name)
# # print('sign', message_digest)

# decrypted_message_digest = decrypt(encrypted_message_digest, pub, n)
# print('fungsi decrypt', decrypted_message_digest)

# # tadi yang kanan

# # decrypted_message_digest = decrypt(encrypted_message_digest, pub, n)
# # print('fungsi decrypt', decrypted_message_digest)

# get_message(file_name)

# message = file_read("message.txt")
# # print('akhir', message)

# hashed_received_md = to_dec(digest(message))
# # print('digest_message', hashed_received_md)

# # dec_hashed_received_md = hashed_received_md
# # # print('decimal', dec_hashed_received_md)

# result_received_md = hashed_received_md % n
# print('hasil', result_received_md)

# authenticate()
