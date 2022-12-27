# Domain Cached Credential (DCC)


---

## Step by Step description

### 1. Prepare username and password



### 2. Compute MD4 of the encoded password



### 3. Compute the MD4 hash of the nthash and the username



## Example

Using the attached [nt-hash-from-password.py](./nt-hash-from-password.py) python script, we can see the step by step values for computing the NT hash:

```
$ ./dcc-hash-from-password.py -u Podalirius -p 'WCExplained!'
[+] Step 1: Prepare username and password
   [+] Raw password (utf-16-le): b'W\x00C\x00E\x00x\x00p\x00l\x00a\x00i\x00n\x00e\x00d\x00!\x00'
   [+] Raw lowercase username (utf-16-le): b'p\x00o\x00d\x00a\x00l\x00i\x00r\x00i\x00u\x00s\x00'

[+] Step 2: Compute NT hash
   [+] Raw NT hash (utf-16-le): b'\x8b\xd3b|\xc4\xa8\xda\x94\xd8\x8fz$Bh\x99\x1d'
   [+] Hex NT hash (utf-16-le): 8bd3627cc4a8da94d88f7a244268991d

[+] Step 3: Compute the MD4 hash of the nthash and the username
   [+] Raw DCC1 hash: b'\xf2m\x84\xa5\x80\xac\x82\xf5\x12\xa2\x97X\xd7#\x01\xa6'

[+] Step 4: We have the final DCC hash
   [+] Hex DCC1 hash: f26d84a580ac82f512a29758d72301a6
   [+] Hashcat format: f26d84a580ac82f512a29758d72301a6:Podalirius
```

If you get a `ValueError: unsupported hash type md4`, this means your OpenSSL installation does not support MD4. You can re-enable it simply by adding this in `/usr/lib/openssl.cnf` or in `/etc/ssl/openssl.cnf`:

```conf
[provider_sect]
default = default_sect
legacy = legacy_sect

[default_sect]
activate = 1

[legacy_sect]
activate = 1
```

Source: https://stackoverflow.com/a/72807264

## References
 - https://openwall.info/wiki/john/MSCash
