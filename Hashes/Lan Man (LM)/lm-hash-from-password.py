#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File name          : lm-hash-from-password.py
# Author             : Podalirius (@podalirius_)
# Date created       : 17 Dec 2022

import argparse
import binascii
# python3 -m pip install pycryptodome
from Crypto.Cipher import DES
from Crypto.Util.number import bytes_to_long, long_to_bytes


def partity_adjust(key):
    def parity_bit(n):
        n = int(n,2)
        parity = 1
        while (n != 0):
            if ((n & 1) == 1):
                parity ^= 1
            n >>= 1
        return str(parity)
    int_key = bytes_to_long(key)
    bin_key = bin(int_key)[2:].rjust(len(key)*8,'0')
    elements = []
    max_elements = (len(key)*8) // 7
    for block_id in range(max_elements):
        # Keep 7 first bits
        A = bin_key[7*(block_id):7*(block_id+1)]
        A = A + parity_bit(A)
        elements.append(A)
    key = long_to_bytes(int(''.join(elements),2))
    return key


def parseArgs():
    parser = argparse.ArgumentParser(description="Description message")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-p", "--password", default=None, help='Password to hash in NTLMv1')
    group.add_argument("-x", "--hex-password", default=None, help='Password to hash in NTLMv1')
    parser.add_argument("-v", "--verbose", default=False, action="store_true", help='Verbose mode. (default: False)')
    return parser.parse_args()


if __name__ == '__main__':
    options = parseArgs()

    lm_secret = b"KGS!@#$%"

    data = None
    if options.password is not None:
        data = bytes(options.password, 'utf-8')

    if options.hex_password is not None:
        data = bytes(binascii.unhexlify(options.hex_password), 'utf-8')

    if data is not None:
        print("[+] Raw password: %s" % data)
        data = data.upper()
        data = data + (14 - len(data))*b'\x00'
        print("[+] Upper raw password: %s" % data)

        k1 = data[0:7]
        print("[+] Message part 1: %s | %s" % (binascii.hexlify(k1).decode('utf-8'), k1))
        k1 = partity_adjust(k1)
        print("  | parity_adjust(K1) = %s" % binascii.hexlify(k1).decode('utf-8'))
        des_ctx = DES.new(k1, DES.MODE_ECB)
        CT1 = des_ctx.encrypt(lm_secret)
        print("  | CT1 = %s" % binascii.hexlify(CT1).decode('utf-8'))

        k2 = data[7:14]
        print("[+] Message part 2: %s | %s" % (binascii.hexlify(k2).decode('utf-8'), k2))
        k2 = partity_adjust(k2)
        print("  | parity_adjust(K2) = %s" % binascii.hexlify(k2).decode('utf-8'))
        des_ctx = DES.new(k2, DES.MODE_ECB)
        CT2 = des_ctx.encrypt(lm_secret)
        print("  | CT2 = %s" % binascii.hexlify(CT2).decode('utf-8'))

        lm_hash = CT1 + CT2
        lm_hash_hex = binascii.hexlify(lm_hash).decode('utf-8')
        print("[+] Raw LM hash: %s" % lm_hash)
        print("[+] LM hash: %s" % lm_hash_hex)
    else:
        pass
