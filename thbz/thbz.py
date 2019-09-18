#!/usr/bin/env python3
#coding:utf-8

from binascii import hexlify, unhexlify
from base64 import b64encode, b64decode

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

__all__ = [
	"str2bin",
	"bin2str",
	"str2hex",
	"hex2str",
	"str2b64",
	"b642str",
	"int2str",
	"str2int"
]

### CONVERSIONS ###

def str2bin(string):
	""" Converts a plain string (string) to a binary sequence (string) """
	converted = ""
	for x in string:
		byt = str(bin(ord(x)))[2:]
		l = len(byt)
		if l < 8:
			byt = '0'*(8-l) + byt
		converted += byt
	return converted

def bin2str(binary):
	""" Converts a binary sequence (string) to a plain string (string) """
	return ''.join(chr(int(binary[i:i+8], 2)) for i in range(0, len(binary), 8))

def str2hex(string):
	""" Converts a plain string (string) to a hexadecimal sequence (string) """
	return str(hexlify(string.encode()))[2:-1]

def hex2str(hexa):
	""" Converts a hexadecimal sequence (string) to a plain string (string) """
	return str(unhexlify(hexa))[2:-1]

def str2b64(string):
	""" Converts a plain string (string) to a base64 sequence (string) """
	return str(b64encode(string.encode()))[2:-1]

def b642str(b64):
	""" Converts a base64 sequence (string) to a plain string (string) """
	return str(b64decode(b64))[2:-1]

def int2str(number):
	""" Converts an integer (int) to a plain string (string) """
	return str(unhexlify(hex(number)[2:]))[2:-1]

def str2int(string):
	""" Converts a plain string (string) to an integer (int) """
	return int(hexlify(string.encode()), 16)


####################

if __name__ == '__main__':
	author()
