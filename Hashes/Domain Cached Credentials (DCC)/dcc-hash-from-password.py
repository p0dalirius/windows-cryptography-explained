#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File name          : dcc-hash-from-password.py
# Author             : Podalirius (@podalirius_)
# Date created       : 17 Dec 2022

import hashlib
import argparse
import binascii


def parseArgs():
    parser = argparse.ArgumentParser(description="Description message")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-p", "--password", default=None, help='Password to hash in DCC')
    group.add_argument("-x", "--hex-password", default=None, help='Password to hash in DCC')
    parser.add_argument("-u", "--username", default=None, required=True, help='Username')
    parser.add_argument("-r", "--rounds", default=10240, required=False, type=int, help='Number of rounds (default: 10240)')
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
        print("[+] Step 1: Prepare username and password")
        print("   [+] Raw password (utf-16-le): %s" % password)
        username = bytes(options.username, 'utf-16-le').lower()
        print("   [+] Raw lowercase username (utf-16-le): %s" % username)
        print()

        print("[+] Step 2: Compute NT hash")
        ctx = hashlib.new('md4', password)
        nthash = ctx.digest()
        print("   [+] Raw NT hash (utf-16-le): %s" % ctx.digest())
        print("   [+] Hex NT hash (utf-16-le): %s" % ctx.hexdigest())
        print()

        print("[+] Step 3: Compute the MD4 hash of the nthash and the username")
        blob = nthash + username
        ctx = hashlib.new('md4', blob)
        print("   [+] Raw DCC1 hash: %s" % ctx.digest())
        print()

        print("[+] Step 4: We have the final DCC hash")
        print("   [+] Hex DCC1 hash: %s" % ctx.hexdigest())
        print("   [+] Hashcat format: %s:%s" % (ctx.hexdigest(), options.username))
    else:
        pass
