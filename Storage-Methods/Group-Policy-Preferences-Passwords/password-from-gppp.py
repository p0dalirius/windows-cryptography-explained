#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File name          : dcc-hash-from-password.py
# Author             : Podalirius (@podalirius_)
# Date created       : 17 Dec 2022

import hashlib
import argparse
import binascii
import base64
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad


def parseArgs():
    parser = argparse.ArgumentParser(description="Description message")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-c", "--cpassword", default=None, help='GPPP encrypted password')
    parser.add_argument("-v", "--verbose", default=False, action="store_true", help='Verbose mode. (default: False)')
    return parser.parse_args()


if __name__ == '__main__':
    options = parseArgs()

    print("[+] Step 1: Prepare the encrypted password")
    print("   [+] Add base64 padding and decode it.")
    pw_enc_b64 = options.cpassword
    # Padding the ciphertext
    pad = len(pw_enc_b64) % 4
    if pad == 1:
        pw_enc_b64 = pw_enc_b64[:-1]
    elif pad == 2 or pad == 3:
        pw_enc_b64 += '=' * (4 - pad)
    pw_enc = base64.b64decode(pw_enc_b64)
    print()


    print("[+] Step 2: Decrypt it with AES(iv=0, mode=CBC, key=...)")
    # AES Key : https://docs.microsoft.com/en-us/openspecs/windows_protocols/ms-gppref/2c15cbf0-f086-4c74-8b70-1f2fa45dd4be)
    key = b'\x4e\x99\x06\xe8\xfc\xb6\x6c\xc9\xfa\xf4\x93\x10\x62\x0f\xfe\xe8\xf4\x96\xe8\x06\xcc\x05\x79\x90\x20\x9b\x09\xa4\x33\xb6\x6c\x1b'
    # Fixed null IV
    iv = b'\x00' * 16
    ctx = AES.new(key, AES.MODE_CBC, iv)
    password = unpad(ctx.decrypt(pw_enc), ctx.block_size)
    print("   [+] Raw decrypted password = %s" % password)
    print()


    print("[+] Step 3: We have the final Group Policy Preferences decrypted cpassword")
    password = password.decode('utf-16-le')
    print("   [+] password = %s" % (password))
