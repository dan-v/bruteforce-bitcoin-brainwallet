# Crypto functions borrowed from Joric/bitcoin-dev
import hashlib
import ctypes
import ctypes.util
import urllib2
import sys
import codecs

ssl = ctypes.cdll.LoadLibrary (ctypes.util.find_library ('ssl') or 'libeay32')

def check_result (val, func, args):
    if val == 0: raise ValueError 
    else: return ctypes.c_void_p (val)

ssl.EC_KEY_new_by_curve_name.restype = ctypes.c_void_p
ssl.EC_KEY_new_by_curve_name.errcheck = check_result

class KEY:
    def __init__(self):
        NID_secp256k1 = 714
        self.k = ssl.EC_KEY_new_by_curve_name(NID_secp256k1)
        self.compressed = False
        self.POINT_CONVERSION_COMPRESSED = 2
        self.POINT_CONVERSION_UNCOMPRESSED = 4

    def __del__(self):
        if ssl:
            ssl.EC_KEY_free(self.k)
        self.k = None

    def generate(self, secret=None):
        if secret:
            priv_key = ssl.BN_bin2bn(secret, 32, ssl.BN_new())
            group = ssl.EC_KEY_get0_group(self.k)
            pub_key = ssl.EC_POINT_new(group)
            ctx = ssl.BN_CTX_new()
            ssl.EC_POINT_mul(group, pub_key, priv_key, None, None, ctx)
            ssl.EC_KEY_set_private_key(self.k, priv_key)
            ssl.EC_KEY_set_public_key(self.k, pub_key)
            ssl.EC_POINT_free(pub_key)
            ssl.BN_CTX_free(ctx)
            return self.k
        else:
            return ssl.EC_KEY_generate_key(self.k)

    def set_privkey(self, key):
        self.mb = ctypes.create_string_buffer(key)
        ssl.d2i_ECPrivateKey(ctypes.byref(self.k), ctypes.byref(ctypes.pointer(self.mb)), len(key))

    def set_pubkey(self, key):
        self.mb = ctypes.create_string_buffer(key)
        ssl.o2i_ECPublicKey(ctypes.byref(self.k), ctypes.byref(ctypes.pointer(self.mb)), len(key))

    def get_privkey(self):
        size = ssl.i2d_ECPrivateKey(self.k, 0)
        mb_pri = ctypes.create_string_buffer(size)
        ssl.i2d_ECPrivateKey(self.k, ctypes.byref(ctypes.pointer(mb_pri)))
        return mb_pri.raw

    def get_pubkey(self):
        size = ssl.i2o_ECPublicKey(self.k, 0)
        mb = ctypes.create_string_buffer(size)
        ssl.i2o_ECPublicKey(self.k, ctypes.byref(ctypes.pointer(mb)))
        return mb.raw

    def get_secret(self):
        bn = ssl.EC_KEY_get0_private_key(self.k);
        bytes = (ssl.BN_num_bits(bn) + 7) / 8
        mb = ctypes.create_string_buffer(bytes)
        n = ssl.BN_bn2bin(bn, mb);
        return mb.raw.rjust(32, chr(0))

    def set_compressed(self, compressed):
        self.compressed = compressed
        if compressed:
            form = self.POINT_CONVERSION_COMPRESSED
        else:
            form = self.POINT_CONVERSION_UNCOMPRESSED
        ssl.EC_KEY_set_conv_form(self.k, form)

def dhash(s):
    return hashlib.sha256(hashlib.sha256(s).digest()).digest()

def rhash(s):
    h1 = hashlib.new('ripemd160')
    h1.update(hashlib.sha256(s).digest())
    return h1.digest()

b58_digits = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'

def base58_encode(n):
    l = []
    while n > 0:
        n, r = divmod(n, 58)
        l.insert(0,(b58_digits[r]))
    return ''.join(l)

def base58_decode(s):
    n = 0
    for ch in s:
        n *= 58
        digit = b58_digits.index(ch)
        n += digit
    return n

def base58_encode_padded(s):
    res = base58_encode(int('0x' + s.encode('hex'), 16))
    pad = 0
    for c in s:
        if c == chr(0):
            pad += 1
        else:
            break
    return b58_digits[0] * pad + res

def base58_decode_padded(s):
    pad = 0
    for c in s:
        if c == b58_digits[0]:
            pad += 1
        else:
            break
    h = '%x' % base58_decode(s)
    if len(h) % 2:
        h = '0' + h
    res = h.decode('hex')
    return chr(0) * pad + res

def base58_check_encode(s, version=0):
    vs = chr(version) + s
    check = dhash(vs)[:4]
    return base58_encode_padded(vs + check)

def base58_check_decode(s, version=0):
    k = base58_decode_padded(s)
    v0, data, check0 = k[0], k[1:-4], k[-4:]
    check1 = dhash(v0 + data)[:4]
    if check0 != check1:
        raise BaseException('checksum error')
    if version != ord(v0):
        raise BaseException('version mismatch')
    return data

def gen_eckey(passphrase=None, secret=None, pkey=None, compressed=False, rounds=1):
    k = KEY()
    if passphrase:
        secret = passphrase.encode('utf8')
        for i in xrange(rounds):
            secret = hashlib.sha256(secret).digest()
    if pkey:
        secret = base58_check_decode(pkey, 128)
        compressed = len(secret) == 33
        secret = secret[0:32]
    k.generate(secret)
    k.set_compressed(compressed)
    return k

def get_addr(k):
    pubkey = k.get_pubkey()
    secret = k.get_secret()
    hash160 = rhash(pubkey)
    addr = base58_check_encode(hash160)
    payload = secret
    if k.compressed:
        payload = secret + chr(1)
    pkey = base58_check_encode(payload, 128)
    return addr, pkey

def test():
    # random uncompressed
    print get_addr(gen_eckey())
    # random compressed
    print get_addr(gen_eckey(compressed=True))
    # by secret
    print get_addr(gen_eckey(secret=('%064x' % 0xdeadbabe).decode('hex')))
    # by passphrase
    print get_addr(gen_eckey(passphrase='Satoshi Nakamoto'))
    # by private key, uncompressed
    print get_addr(gen_eckey(pkey='5K1HkbYffstTZDuV4riUWMbAMkQh57b8798uoy9pXYUDYeUHe7F'))
    # by private key, compressed
    print get_addr(gen_eckey(pkey='L3ATL5R9Exe1ubuAnHVgNgTKZEUKkDvWYAWkLUCyyvzzxRjtgyFe'))

if __name__ == '__main__':
    dict_file = "dictionary.txt"
    found_file = "found_addresses.txt"
    abe_server = "localhost"
    abe_port = "2750"
    abe_chain = "Bitcoin"
    print "Starting search for used brainwallet addresses using dictionary '%s'" % dict_file

    num_lines = sum(1 for line in open(dict_file))

    line_count = 0
    found = codecs.open(found_file,'a','utf8')
    dictionary = codecs.open(dict_file,'r','utf8')
    for raw_line in dictionary:
        line_count += 1
        line = raw_line.rstrip()
        a = get_addr(gen_eckey(passphrase=line))
        address = a[0]
        private_address = a[1]
        try:
            url = "http://%s:%s/chain/%s/q/getreceivedbyaddress/%s" % (abe_server, abe_port, abe_chain, address)
            received_bitcoins = urllib2.urlopen(url).read()
        except urllib2.URLError:
            print "Request failed for word '%s' to URL '%s'" % (line, url)
            continue
			
        if(received_bitcoins != "0"):
            msg = "Found address %s using dictionary word %s which has received %s bitcoins. Private key: %s\n" % (address, line.rstrip(), received_bitcoins, private_address)
            print msg
            found.write(msg)
        if( (line_count % 1000) == 0 ):
            print "Progress: %s of %s words checked so far" % (line_count, num_lines)
            
    found.close()
    dictionary.close()
