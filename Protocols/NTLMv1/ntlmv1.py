#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File name          : ntlmv1-from-password.py
# Author             : Podalirius (@podalirius_)
# Date created       : 16 Dec 2022

import hashlib
import argparse
import binascii
# python3 -m pip install pycryptodome
from Crypto.Cipher import DES
from Crypto.Util.number import bytes_to_long, long_to_bytes
import sys

# Administrator::COERCE:5977A887FCBCB3C4CB9D3F6EAD171BA36D6C077F87B97B2E:5977A887FCBCB3C4CB9D3F6EAD171BA36D6C077F87B97B2E:1122334455667788

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
    parser.add_argument("-c", "--challenge", default="1122334455667788", required=False, help='Password to hash in NTLMv1')
    parser.add_argument("-e", "--expected-response", default=None, required=False, help='NTLMv1 hash response')
    parser.add_argument("-v", "--verbose", default=False, action="store_true", help='Verbose mode. (default: False)')
    return parser.parse_args()


if __name__ == '__main__':
    options = parseArgs()

    if len(options.challenge) != 16:
        print("[!] Invalid challenge length (%d) should be 16." % len(options.challenge))
        sys.exit(0)

    C = binascii.unhexlify(options.challenge)
    print("[+] Server challenge: %s | hex: %s" % (C, options.challenge))

    data = None
    if options.password is not None:
        data = bytes(options.password, 'utf-16-le')

    if options.hex_password is not None:
        data = bytes(binascii.unhexlify(options.hex_password), 'utf-16-le')

    if data is not None:
        print("[+] Raw password: %s" % data)
        ctx = hashlib.new('md4', data)
        nt_hash_value = ctx.hexdigest()
        raw_keys = ctx.digest() + (b'\x00')*(3*7 - len(ctx.digest()))
        print("[+] NT hash: %s" % nt_hash_value)
        print("[+] NTLM-Hash | 5-bytes-0: %s" % (nt_hash_value + '00' * 5))

        print("[+] Computing block 1")
        K1 = raw_keys[0:7]
        K1_hex = binascii.hexlify(K1).decode('utf-8')
        print("  | K1 = %s | hex: %s" % (K1, K1_hex))
        K1 = partity_adjust(K1)
        print("  | parity_adjust(K1) = %s" % binascii.hexlify(K1).decode('utf-8'))
        des_ctx = DES.new(K1, DES.MODE_ECB)
        CT1 = des_ctx.encrypt(C)
        print("  | DES(key='%s').encrypt('%s') = %s" % (K1_hex, options.challenge, CT1))
        print("  | CT1 = %s" % binascii.hexlify(CT1).decode('utf-8'))

        print("[+] Computing block 2")
        K2 = raw_keys[7:14]
        K2_hex = binascii.hexlify(K2).decode('utf-8')
        print("  | K2 = %s | hex: %s" % (K2, K2_hex))
        K2 = partity_adjust(K2)
        print("  | parity_adjust(K2) = %s" % binascii.hexlify(K2).decode('utf-8'))
        des_ctx = DES.new(K2, DES.MODE_ECB)
        CT2 = des_ctx.encrypt(C)
        print("  | DES(key='%s').encrypt('%s') = %s" % (K2_hex, options.challenge, CT2))
        print("  | CT2 = %s" % binascii.hexlify(CT2).decode('utf-8'))

        print("[+] Computing block 3")
        K3 = raw_keys[14:28]
        K3_hex = binascii.hexlify(K3).decode('utf-8')
        print("  | K3 = %s | hex: %s" % (K3, K3_hex))
        K3 = partity_adjust(K3)
        print("  | parity_adjust(K3) = %s" % binascii.hexlify(K3).decode('utf-8'))
        des_ctx = DES.new(K3, DES.MODE_ECB)
        CT3 = des_ctx.encrypt(C)
        print("  | DES(key='%s').encrypt('%s') = %s" % (K3_hex, options.challenge, CT3))
        print("  | CT3 = %s" % binascii.hexlify(CT3).decode('utf-8'))

        response = CT1 + CT2 + CT3
        response_hex = binascii.hexlify(response).decode('utf-8').upper()
        print("[+] CT1 + CT2 + CT3: %s" % response_hex)

        if options.expected_response is not None:
            diff_hex = ""
            expected = "19567EECB51A31E36FFE3EB9D7D576E44C379F5A7C79F980".upper()
            for k in range(len(response_hex)):
                if response_hex[k] == expected[k]:
                    diff_hex += "\x1b[1;92m" + response_hex[k] + "\x1b[0m"
                else:
                    diff_hex += "\x1b[1;91m" + response_hex[k] + "\x1b[0m"
            print("\n[+] NTLMv1 hash: %s" % diff_hex)
            print("       should be %s" % expected)
        else:
            print("\n[+] NTLMv1 hash: %s" % response_hex)

    else:
        pass