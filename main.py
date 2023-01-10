# Algorithm 1 LFSR
import math
from pathlib import Path
from PIL import Image

def LFSR(seed):
    seq = '{:032b}'.format(seed, 'b')  # 32 bit binary representation

    seq_list = list(seq)
    x = int(seq[7])
    y = int(seq[18])
    z = int(seq[31])

    xor = str(x ^ y ^ z)

    for i in range(31):
        seq_list[i+1] = seq[i]
    seq_list[0] = xor

    # Return decimal representation
    result = "".join(seq_list)
    num = int(result, 2)

    return num, xor


# Algorithm 2 LFSR_USE
def LFSR_USE(seed):
    z = LFSR(seed)
    s = [z[1]]
    p = z[0]

    for i in range(7):
        z = LFSR(p)
        s.append(z[1])
        p = z[0]
    new = z[0]

    result = "".join(s)
    n = int(result, 2)

    return n, new


# Algorithm 4 RC4(k)
def RC4(key):
    K = []
    S = []
    T = []
    keylen = math.floor(math.log2(key))
    for i in range(keylen+1):
        K.append(key % 256)
        key = math.floor(key/256)
    for i in range(256):
        S.append(i)
        T.append(K[i % keylen])
    j = 0
    for i in range(256):
        j = (j + S[i]+T[i]) % 256
        S[i], S[j] = S[j], S[i]
    return S


# Algorithm 3 RC4_USE
def RC4_USE(key, m, n):
    S = RC4(key)
    m = (m+1) % 256
    n = n + S[m] % 256
    S[m], S[m] = S[n], S[m]
    key = S[(S[m]+S[n]) % 256]

    return key, m, n


# Algorithm 5 Encrypt_Color
def ENCRYPT_COLOR(key, height, width):
    x = key
    k = (0, 0, 0)
    nr = LFSR_USE(x)[1]
    for i in range(width):
        nc = LFSR_USE(nr)[0]
        for j in range(height):
            r, g, b= pix_map[i, j]
            r = r + nc
            g = g + nc
            b = b + nc
            # p = p + nc
            pix_map[i, j] = (r, g, b)
            r = RC4_USE(key, k[1], k[2])
            nc = (nc + r[0]) % 256
        nr = LFSR_USE(nr)[1]


# Algorithm 6 is_prime
def IS_PRIME(number):
    sqrt = math.floor(math.sqrt(number))
    for i in range(2, sqrt):
        if number % i == 0:
            return False
    return True


# Algorithm 7 prime
def PRIME(number):
    for i in range(number+1, 2*number):
        if IS_PRIME(i):
            return i


# Algorithm 8 CIG
def CIG(primes):
    ret_list = []
    list_t = []
    T = 1
    for x in primes:
        T = T*x
    for x in primes:
        list_t.append(T/x)
    for i in range(T):
        S = 0
        for j in range(len(primes)):
            S = S + list_t[j]*i
        S = S % T
        ret_list.append(S)
    return ret_list


# Algorithm 9
def CIG_USE(list, limit):
    for x in list:
        if x > limit:
            list.remove(x)


# Algorithm 10
def FIND(position, height, width):
    return math.floor(position/width), position % width


# Algorithm 11
def SWAP(list, width, height):
    C = 0
    for i in range(int(height/2), height):
        for j in range(width):
            position = list[C]
            C = C + 1
            X = FIND(position, height, width)
            pix_map[i, j], pix_map[X[0], X[1]] = pix_map[X[0], X[1]], pix_map[i, j]


# Algorithm 12
def ENCRYPT_POSITION(height, width):
    limit = height*width/2
    h = PRIME(int(height/2))
    w = PRIME(width)
    cig_list = CIG([h, w])
    CIG_USE(cig_list, limit)
    SWAP(cig_list, height, width)


# Algorithm 13
def Encryption(key, height, width):
    ENCRYPT_COLOR(key, height, width)
    ENCRYPT_POSITION(height, width)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    try:
        path = Path("Picture1.jpg")
        file_name = path.name
        file_name = "encrypt"+file_name
        img = Image.open(path, 'r')
        pix_map = img.load()
        width, height = img.size
        # Encryption(1000, int(height/2), int(width/2))
        Encryption(1000, height, width)
        # ENCRYPT_COLOR(100, int(height/2), int(width/2))
        img.show()
        img.save(file_name)
    except IOError:
        pass
