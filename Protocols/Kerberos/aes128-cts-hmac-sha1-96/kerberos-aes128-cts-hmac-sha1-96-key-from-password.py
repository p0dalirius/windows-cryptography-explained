#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File name          : kerberos-aes128-cts-hmac-sha1-96-key-from-password.py
# Author             : Podalirius (@podalirius_)
# Date created       : 16 Dec 2022

import hashlib
import argparse
import binascii
# python3 -m pip install pycryptodome
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad


def parseArgs():
    parser = argparse.ArgumentParser(description="Description message")
    parser.add_argument("-u", "--username", required=True, help="Username of the account")
    parser.add_argument("-d", "--domain", default='', required=False, help="Domain of the account")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-p", "--password", default=None, help="Password to hash in NTLMv1")
    group.add_argument("-x", "--hex-password", default=None, help="Password to hash in NTLMv1")
    parser.add_argument("-v", "--verbose", default=False, action="store_true", help="Verbose mode. (default: False)")
    parser.add_argument("-i", "--iterations", default=4096, required=False, type=int, help="Number of iterations to use in the PBKDF2. (default: 4096)")
    return parser.parse_args()


if __name__ == '__main__':
    options = parseArgs()

    domain = None
    if options.domain is not None:
        domain = bytes(options.domain, 'utf-8')

    username = None
    if options.username is not None:
        username = bytes(options.username, 'utf-8')

    password = None
    if options.password is not None:
        password = bytes(options.password, 'utf-8')
    elif options.hex_password is not None:
        password = bytes(binascii.unhexlify(options.hex_password), 'utf-8')

    print("[+] Computing salt:")
    print("  | domain   = %s" % domain)
    print("  | username = %s" % username)
    salt = domain.upper() + username
    print("  | salt = %s" % salt)
    print()

    print("[+] Computing PBKDF2-HMAC from password:")
    print("  | username = %s" % username)
    K = hashlib.pbkdf2_hmac(
        hash_name='sha1',
        password=password,
        salt=salt, 
        iterations=options.iterations, 
        dklen=16
    )
    K_hex =  binascii.hexlify(K).decode("utf-8")
    print("  | PBKDF2(salt+password) = %s" % K_hex)
    print()

    IV = binascii.unhexlify("00000000000000000000000000000000")
    KerberosConstant = binascii.unhexlify("6b65726265726f737b9b5b2b93132b935c9bdcdad95c9899c4cae4dee6d6cae4")

    print("[+] Encrypting constant with AES:")
    aes_ctx_ct1 = AES.new(key=K, mode=AES.MODE_CBC, iv=IV)
    CT1 = aes_ctx_ct1.encrypt(pad(KerberosConstant, AES.block_size))
    print("  | AES(key='%s').encrypt(KerberosConstant) = %s" % (K_hex, CT1))
    print("  | CT1 = %s" % binascii.hexlify(CT1).decode('utf-8'))
    print()

    print("[+] Concatenating values:")
    CT1 = CT1[:16]
    print("  | CT1[:16] = %s" % binascii.hexlify(CT1).decode('utf-8'))
    identity = options.username
    if len(options.domain) != 0:
        identity = options.domain.upper() + '\\' + identity
    print("  | Kerberos aes128-cts-hmac-sha1-96 key for '%s': %s" % (identity, binascii.hexlify(CT1).decode('utf-8')))
    print()
