#!/usr/bin/env python3
#coding:utf-8

from binascii import hexlify, unhexlify
from base64 import b64encode, b64decode
from datetime import datetime

def author():
	print("              _   _     _        ")
	print("             | | | |   | |       ")
	print("  _ __  _   _| |_| |__ | |__ ____")
	print(" | '_ \| | | | __| '_ \| '_ \_  /")
	print(" | |_) | |_| | |_| | | | |_) / / ")
	print(" | .__/ \__, |\__|_| |_|_.__/___|")
	print(" | |     __/ |                   ")
	print(" |_|    |___/                    ")
	print()
	print("@thbz__")
	print("https://thbz.fr")


### CONVERSIONS ###

def str2bin(string):
	converted = ""
	for x in string:
		byt = str(bin(ord(x)))[2:]
		l = len(byt)
		if l < 8:
			byt = '0'*(8-l) + byt
		converted += byt
	return converted

def bin2str(binary):
	return ''.join(chr(int(binary[i:i+8], 2)) for i in range(0, len(binary), 8))

def str2hex(string):
	return str(hexlify(string.encode()))[2:-1]

def hex2str(hexa):
	return str(unhexlify(hexa))[2:-1]

def str2b64(string):
	return str(b64encode(string.encode()))[2:-1]

def b642str(b64):
	return str(b64decode(b64))[2:-1]

def int2str(number):
    return str(unhexlify(hex(number)[2:]))[2:-1]

def str2int(string):
	return int(binascii.hexlify(string.encode()), 16)


####################

if __name__ == '__main__':
	author()
