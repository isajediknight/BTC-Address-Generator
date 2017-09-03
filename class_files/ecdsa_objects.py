import ecdsa,binascii, hashlib, datetime, os

secp256k1curve=ecdsa.ellipticcurve.CurveFp(115792089237316195423570985008687907853269984665640564039457584007908834671663,0,7)
secp256k1point=ecdsa.ellipticcurve.Point(secp256k1curve,0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798,0x483ADA7726A3C4655DA4FBFC0E1108A8FD17B448A68554199C47D08FFB10D4B8,0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141)
secp256k1=ecdsa.curves.Curve('secp256k1',secp256k1curve,secp256k1point,(1,3,132,0,10))

def addy(pk):
    """
    Generates a first generation BTC Address
    """
    pko=ecdsa.SigningKey.from_secret_exponent(pk,secp256k1)
    pubkey=binascii.hexlify(pko.get_verifying_key().to_string())
    pubkey2=hashlib.sha256(binascii.unhexlify('04'+pubkey)).hexdigest()
    pubkey3=hashlib.new('ripemd160',binascii.unhexlify(pubkey2)).hexdigest()
    pubkey4=hashlib.sha256(binascii.unhexlify('00'+pubkey3)).hexdigest()
    pubkey5=hashlib.sha256(binascii.unhexlify(pubkey4)).hexdigest()
    pubkey6=pubkey3+pubkey5[:8]
    pubnum=int(pubkey6,16)
    pubnumlist=[]
    while pubnum!=0: pubnumlist.append(pubnum%58); pubnum/=58
    address=''
    for l in ['123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'[x] for x in pubnumlist]:
        address=l+address
    return address

def baseN(num, base, numerals="0123456789abcdefghijklmnopqrstuvwxyz"):
    """
    Convert any int to base/radix 2-36 string. Special numerals can be used
    to convert to any base or radix you need. This function is essentially
    an inverse int(s, base).

    For example:
    >>> baseN(-13, 4)
    '-31'
    >>> baseN(91321, 2)
    '10110010010111001'
    >>> baseN(791321, 36)
    'gyl5'
    >>> baseN(91321, 2, 'ab')
    'babbaabaababbbaab'
    """
    if num == 0:
        return "0"

    if num < 0:
        return '-' + baseN((-1) * num, base, numerals)

    if not 2 <= base <= len(numerals):
        raise ValueError('Base must be between 2-%d' % len(numerals))

    left_digits = num // base
    if left_digits == 0:
        return numerals[num % base]
    else:
        return baseN(left_digits, base, numerals) + numerals[num % base]

def privkey():
    """
    Generate a random private key
    """
    a = ''
    b = ''
    for x in range(0,32):
        b = baseN(ord(os.urandom(1)),16,'0123456789ABCDEF')
        if(len(b) == 1):
            b = '0' + b
        a += b
    return a

def new_baseN(num,b,numerals="0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"):
    return ((num == 0) and  "0" ) or ( new_baseN(num // b, b).lstrip("0") + numerals[num % b])

def bit_baseN(num,b,numerals="123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"):
    return ((num == 0) and  "0" ) or( bit_baseN(num // b, b).lstrip("0") + numerals[num % b])
