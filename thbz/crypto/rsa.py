#!/usr/bin/env python3
#coding:utf-8

from thbz import *

from sys import setrecursionlimit
from os import chmod

from base64 import b64encode, b64decode
from binascii import hexlify, unhexlify

from Crypto.PublicKey import RSA
from Crypto.Util.number import GCD
from gmpy2 import get_context, invert, powmod, root, sqrt
from sympy.solvers import solve
from sympy import Symbol

from factordb.factordb import FactorDB


def main():
    print("  _   _     _                                    ")
    print(" | | | |   | |                                   ")
    print(" | |_| |__ | |__ ____                            ")
    print(" | __| '_ \| '_ \_  /                            ")
    print(" | |_| | | | |_) / /    _                        ")
    print("  \__|_| |_|_.__/___|  | |                       ")
    print(" ( )__ _ __ _   _ _ __ | |_ ___   _ __ ___  __ _ ")
    print(" |/ __| '__| | | | '_ \| __/ _ \ | '__/ __|/ _` |")
    print(" | (__| |  | |_| | |_) | || (_) || |  \__ \ (_| |")
    print("  \___|_|   \__, | .__/ \__\___(_)_|  |___/\__,_|")
    print("             __/ | |                             ")
    print("            |___/|_|                             ")
    print()

__all__ = [
    "CommonModulus",
    "Facto",
    "MultipleReceivers",
    "Wiener",
    "bezout",
    "load_pk",
    "load_ct",
    "modulus_factors"
]

class CommonModulus:
    def __init__(self, n1, n2, e1, e2, c1, c2):
        self.n = None
        self.n1 = n1
        self.n2 = n2
        self.e1 = e1
        self.e2 = e2
        self.c1 = c1
        self.c2 = c2
        self.m = None

        if self.check_common_modulus():
            self.n = self.n1
            u, v = bezout(self.e1, self.e2)
            self.m = (powmod(self.c1,u,self.n) * powmod(self.c2,v,self.n)) % self.n

    def check_common_modulus(self):
        """
            Verifies that conditions are gathered to make a common modulus attack.
            Returns a boolean.
        """
        if self.n1 == self.n2 and GCD(self.e1, self.e2) == 1:
            self.n = self.n1
            return True
        return False

class Facto:
    def __init__(self, n, e, c):
        self.n = n
        self.e = e
        self.p = None
        self.q = None
        self.d = None
        self.c = c
        self.m = None

        factors = modulus_factors(self.n)
        if len(factors) == 2:
            self.p = factors[0]
            self.q = factors[1]
            self.phi = (self.p-1)*(self.q-1)
            self.d = bezout(self.e, self.phi)[0]
            self.m = pow(self.c,self.d,self.n)

class MultipleReceivers:
    def __init__(self, e, messages_list):
        """
            Example with e = 3, messages_list should be:
            [
                [n1, c1],
                [n2, c2],
                [n3, c3],
            ]
        """

        self.e = e
        self.N = None
        self.m = None

        if len(messages_list) != e:
            return False

        for i in range(e):
            if self.N == None:
                self.N = messages_list[i][0]
            else:
                self.N *= messages_list[i][0]

        for i in range(e):
            ni = messages_list[i][0]
            ci = messages_list[i][1]
            Ni = self.N//ni
            ui = invert(Ni, ni)

            if self.m == None:
                self.m = ci*ui*Ni
            else:
                self.m += ci*ui*Ni

        self.m = int(root(self.m % self.N, 3))

class Wiener:
    def __init__(self, n, e):
        self.n = n
        self.e = e
        self.p = None
        self.q = None
        self.phi = None
        self.d = None

        setrecursionlimit(100000)
        frac = self.rational_to_contfrac(self.e, self.n)
        convergents = self.convergents_from_contfrac(frac)
        self.p, self.q = self.pq_from_convergents(convergents)
        self.d = bezout(self.e, self.phi)[0]

    def contfrac_to_rational(self, frac):
        if len(frac) == 0:
            return (0, 1)
        elif len(frac) == 1:
            return (frac[0], 1)
        else:
            remainder = frac[1:len(frac)]
            (num, denom) = self.contfrac_to_rational(remainder)
            return (frac[0] * num + denom, num)

    def convergents_from_contfrac(self, frac):
        convs = []
        for i in range(len(frac)):
            convs.append(self.contfrac_to_rational(frac[0:i]))
        return convs

    def pq_from_convergents(self, convergents):
        for (k, d) in convergents:
            if k != 0 and (self.e * d - 1) % k == 0:
                phi = (self.e*d-1)//k
                x = Symbol('x')
                roots = solve(x**2 - ((self.n-phi) + 1)*x + self.n, x)
                if len(roots) == 2:
                    p, q = roots
                    if p*q == self.n:
                        self.p = p
                        self.q = q
                        self.phi = (p-1)*(q-1)
                        return (p, q)
        return (None, None)

    def rational_to_contfrac(self, x, y):
        a = x // y
        if a * y == x:
            return [a]
        else:
            pquotients = self.rational_to_contfrac(y, x - a * y)
            pquotients.insert(0, a)
            return pquotients


### USEFUL ###

def load_pk(filename, format="PEM"):
    """ Loads a public key from filename. Returns a RsaKey object. """

    if format == "PEM":
        return RSA.importKey(open(filename).read())
    return false

def load_ct(filename, enc="base64"):
    """ Loads a cipher text from filename. Returns an int. """

    content = open(filename).read().replace('\n', '')

    if enc == "base64":
        return int(str(hexlify(b64decode(content)))[2:-1], 16)
    elif enc == "hex":
        return int(content, 16)
    return false

def modulus_factors(n):
    """
        Queries factordb to get a modulus' factors.
        Returns a tuple of integers.
    """

    f = FactorDB(n)
    f.connect()
    return f.get_factor_list()


### ALGO ###

def bezout(e, phi):
    """
        Calculate RSA private key from e and phi, using Bezout's theorem.
        Returns an integer.
    """
    a, b = e, phi
    if b == 0:
        if a==0:
            return 0,0,0
        return abs(a),-1 if a<0 else 1,0
    a, sa = abs(a), -1 if a<0 else 1
    b, sb = abs(b), -1 if b<0 else 1
    vv, uu, v, u = 1,0,0,1
    e=1
    q, rr = divmod(a, b)
    while rr:
        a, b = b, rr
        vv, v = q*vv + v, vv
        uu, u = q*uu + u, uu
        e = -e
        q, rr = divmod(a, b)
    return int(-sa*e*uu), int(sb*e*vv)


####################

if __name__ == "__main__":
    main()
