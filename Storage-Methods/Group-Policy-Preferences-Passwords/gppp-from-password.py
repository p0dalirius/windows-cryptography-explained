#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File name          : dcc-hash-from-password.py
# Author             : Podalirius (@podalirius_)
# Date created       : 17 Dec 2022

import argparse
import binascii
import base64
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad


def parseArgs():
    parser = argparse.ArgumentParser(description="Description message")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-p", "--password", default=None, help='Password to encrypt in GPPP')
    group.add_argument("-x", "--hex-password", default=None, help='Password to encrypt in GPPP')
    parser.add_argument("-v", "--verbose", default=False, action="store_true", help='Verbose mode. (default: False)')
    return parser.parse_args()


if __name__ == '__main__':
    options = parseArgs()

    password = None
    if options.password is not None:
        password = bytes(options.password, 'utf-16-le')

    if options.hex_password is not None:
        password = bytes(binascii.unhexlify(options.hex_password), 'utf-16-le')

    if password is not None:
        print("[+] Step 1: Prepare the password")
        print("   [+] Raw password (utf-16-le): %s" % password)
        print()

        print("[+] Step 2: Encrypt with AES(iv=0, mode=CBC, key=...)")
        # AES Key : https://docs.microsoft.com/en-us/openspecs/windows_protocols/ms-gppref/2c15cbf0-f086-4c74-8b70-1f2fa45dd4be)
        key = b'\x4e\x99\x06\xe8\xfc\xb6\x6c\xc9\xfa\xf4\x93\x10\x62\x0f\xfe\xe8\xf4\x96\xe8\x06\xcc\x05\x79\x90\x20\x9b\x09\xa4\x33\xb6\x6c\x1b'
        # Fixed null IV
        iv = b'\x00' * 16
        ctx = AES.new(key, AES.MODE_CBC, iv)
        password = pad(password, ctx.block_size)
        cpassword = ctx.encrypt(password)
        print("   [+] Raw cpassword = %s" % cpassword)
        print()

        print("[+] Step 3: We have the final Group Policy Preferences encrypted cpassword")
        b64_cpassword = base64.b64encode(cpassword).decode('utf-8').rstrip('=')
        print("   [+] cpassword = %s" % (b64_cpassword))
    else:
        pass
