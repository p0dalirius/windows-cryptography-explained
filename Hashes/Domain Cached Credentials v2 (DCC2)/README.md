# Domain Cached Credential (DCC) v2

Domain Cached Credentials v2 (DCC2) are an updated version of Domain Cached Credentials (DCC) in Windows. They are encrypted and stored in the Windows registry, just like DCC. DCC2 provides enhanced security features compared to DCC.

DCC2 is primarily used in scenarios where a user needs to log in to their Windows account without network connectivity. It allows users to authenticate and access their Windows accounts, files, and applications even when the domain controller is not available. This is particularly useful for users who are traveling or working in remote locations with limited or no network access.

Similar to DCC, DCC2 poses a security risk if an attacker gains physical access to a computer. If the attacker can extract the cached credentials from the Windows registry, they can potentially use them to gain unauthorized access to the user's account and sensitive data. Therefore, it is crucial to use strong passwords and implement additional security measures, such as disk encryption, to protect against such attacks.

---

## Step by Step computation

### 1. Encode password in UTF-16-LE



### 2. Compute NT hash



### 3. Compute the MD4 hash of the nthash and the username



### 4. Applying PBKDF2-HMAC-SHA1 with 10240 rounds to DCC1 hash



## Example

Using the attached [dcc2-hash-from-password.py](./dcc2-hash-from-password.py) python script, we can see the step by step values for computing the NT hash:

```
$ ./dcc2-hash-from-password.py -p 'Podalirius!' -u 'Administrator' -v
[+] Step 1: Prepare username and password
   [+] Raw password (utf-16-le): b'P\x00o\x00d\x00a\x00l\x00i\x00r\x00i\x00u\x00s\x00!\x00'
   [+] Raw lowercase username (utf-16-le): b'a\x00d\x00m\x00i\x00n\x00i\x00s\x00t\x00r\x00a\x00t\x00o\x00r\x00'

[+] Step 2: Compute NT hash
   [+] Raw NT hash (utf-16-le): b'\x12$s\xd7Z\xd1mK(\x02cd\xf6\xc0\xa9x'
   [+] Hex NT hash (utf-16-le): 122473d75ad16d4b28026364f6c0a978

[+] Step 3: Compute the MD4 hash of the nthash and the username
   [+] Raw DCC1 hash: b'H2,HIJAs\x0e\x1a?rV\xd9\x198'
   [+] Hex DCC1 hash: 48322c48494a41730e1a3f7256d91938

[+] Step 4: Applying PBKDF2-HMAC-SHA1 with 10240 rounds to DCC1 hash
   [+] Raw DCC2 hash: b'\xc0\xd0\xbbJ*\xec\xe5[\xbcp\x06\x8ct\xaeG\xf0)\xb4\xb0\x16'
   [+] Raw DCC2 hash: c0d0bb4a2aece55bbc70068c74ae47f0
   [+] Hashcat format: $DCC$10240#Administrator#c0d0bb4a2aece55bbc70068c74ae47f0
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
 - https://openwall.info/wiki/john/MSCash2
