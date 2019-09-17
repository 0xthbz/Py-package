#!/usr/bin/env python3
#coding:utf-8

from Crypto.PublicKey import RSA
from Crypto.Util.number import GCD
from gmpy2 import powmod
from base64 import b64encode, b64decode
from binascii import hexlify, unhexlify

def main():
    print(" _   _     _")
    print("| | | |   | |")
    print("| |_| |__ | |__ ____  _ __ ___  __ _")
    print("| __| '_ \| '_ \_  / | '__/ __|/ _` |")
    print("| |_| | | | |_) / / _| |  \__ \ (_| |")
    print(" \__|_| |_|_.__/___(_)_|  |___/\__,_|")
    print()

__all__ = [
    "flag_common_modulus",
    "check_common_modulus",
    "load_pk",
    "load_ct",
    "bezout"
]


### FLAG ###

def flag_common_modulus(n1, n2, e1, e2, c1, c2):
    """
        Easily recover a message sent twice with a common modulus.
        Returns a string.

        :param int n1: Message 1 modulus
        :param int n2: Message 2 modulus
        :param int e1: Message 1 exponent
        :param int e2: Message 2 exponent
        :param int c1: Message 1 ciphertext
        :param int c2: Message 2 ciphertext
    """

    # Check if common modulus attack is possible
    if not check_common_modulus(n1, n2, e1, e2):
        return False

    n = n1
    u, v = bezout(e1, e2)
    return str(unhexlify(hex(((powmod(c1,u,n) * powmod(c2,v,n)) % n))[2:]))[2:-1]


### CORE ###

def check_common_modulus(n1, n2, e1, e2):
    if n1 == n2 and GCD(e1, e2) == 1:
        return True
    return False

def load_pk(filename, format="pem"):
    if format == "pem":
        return RSA.importKey(open(filename).read())
    return false

def load_ct(filename, enc="base64"):
    if enc == "base64":
        return int(str(hexlify(b64decode(open(filename).read().replace('\n', ''))))[2:-1], 16)
    return false


### ALGO ###

def bezout(a, b):
    if b == 0:
        if a==0:
            return 0,0,0
        return abs(a),-1 if a<0 else 1,0
    a, sa = abs(a), -1 if a<0 else 1
    b, sb = abs(b), -1if b<0 else 1
    vv, uu, v, u = 1,0,0,1
    e=1
    q, rr = divmod(a, b)
    while rr:
        a, b = b, rr
        vv, v = q*vv + v, vv
        uu, u = q*uu + u, uu
        e = -e
        q, rr = divmod(a, b)
    return -sa*e*uu, sb*e*vv


####################

if __name__ == "__main__":
    main()
