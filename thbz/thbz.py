#!/usr/bin/env python3
#coding: utf-8

from binascii import hexlify, unhexlify
from base64 import b64encode, b64decode
from datetime import datetime

def hello():
	print("thbz")
	print("@thbz__")
	print("https://0xthbz.fr")

def date():
    now = datetime.now()
    year, month, day = now.year, '%02d'%now.month, '%02d'%now.day
    hour, minute, second = '%02d'%now.hour, '%02d'%now.minute, '%02d'%now.second
    dic = {
        'year': year,
        'month': month,
        'day': day,
        'hour': hour,
        'minute': minute,
        'second': second
    }
    return dic


# CONVERSIONS

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
	return str(hexlify(string.encode('utf-8')))[2:-1]

def hex2str(hexadecimal):
	return str(unhexlify(hexadecimal))[2:-1]

def str2b64(string):
	return str(b64encode(string.encode('utf-8')))[2:-1]

def b642str(b64):
	return str(b64decode(data))[2:-1]

if __name__ == '__main__':
	hello()
