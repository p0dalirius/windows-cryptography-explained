#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File name          : nt-hash-from-password.py
# Author             : Podalirius (@podalirius_)
# Date created       : 17 Dec 2022

import hashlib
import argparse
import binascii


def parseArgs():
    parser = argparse.ArgumentParser(description="Description message")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-p", "--password", default=None, help='Password to hash in NTLMv1')
    group.add_argument("-x", "--hex-password", default=None, help='Password to hash in NTLMv1')
    parser.add_argument("-v", "--verbose", default=False, action="store_true", help='Verbose mode. (default: False)')
    return parser.parse_args()


if __name__ == '__main__':
    options = parseArgs()

    data = None
    if options.password is not None:
        data = bytes(options.password, 'utf-16-le')

    if options.hex_password is not None:
        data = bytes(binascii.unhexlify(options.hex_password), 'utf-16-le')

    if data is not None:
        print("[+] Raw password (utf-16-le): %s" % data)
        ctx = hashlib.new('md4', data)
        print("[+] Raw NT hash: %s" % ctx.digest())
        print("[+] NT hash: %s" % ctx.hexdigest())
    else:
        pass
