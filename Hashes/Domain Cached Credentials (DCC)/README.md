# Domain Cached Credential (DCC)

Domain Cached Credentials (DCC) are a type of credential used in Windows operating systems. When a user logs into a Windows domain, their credentials are typically stored on the domain controller for future use. However, in some cases, such as when a domain controller is unavailable or when a user logs in offline, Windows stores a copy of the user's credentials locally on the computer in the form of Domain Cached Credentials.

Domain Cached Credentials are encrypted and stored in the Windows registry. They can be accessed and used by Windows to authenticate the user even when the domain controller is not available. This allows users to log in to their Windows accounts and access resources on their computer, such as files and applications, even when they are not connected to the network.

Domain Cached Credentials are primarily used in scenarios where a user needs to log in to their Windows account without network connectivity. For example, if a user is traveling and does not have access to the domain controller, they can still log in to their computer using the cached credentials. Similarly, if a domain controller is temporarily unavailable, users can continue to work on their computers using the cached credentials until the domain controller is back online.

It is important to note that Domain Cached Credentials pose a security risk, as they can be targeted by attackers who gain physical access to a computer. If an attacker can extract the cached credentials from the Windows registry, they can potentially use them to gain unauthorized access to the user's account and sensitive data. Therefore, it is recommended to use strong passwords and implement additional security measures, such as disk encryption, to protect against such attacks.

---

## Step by Step computation

### 1. Prepare username and password



### 2. Compute NT hash



### 3. Compute the MD4 hash of the nthash and the username



### 4. We have the final DCC hash



## Example

Using the attached [dcc-hash-from-password.py](./dcc-hash-from-password.py) python script, we can see the step by step values for computing the NT hash:

```
$ ./dcc-hash-from-password.py -p 'Podalirius!' -u 'Administrator' -v
[+] Step 1: Prepare username and password
   [+] Raw password (utf-16-le): b'P\x00o\x00d\x00a\x00l\x00i\x00r\x00i\x00u\x00s\x00!\x00'
   [+] Raw lowercase username (utf-16-le): b'a\x00d\x00m\x00i\x00n\x00i\x00s\x00t\x00r\x00a\x00t\x00o\x00r\x00'

[+] Step 2: Compute NT hash
   [+] Raw NT hash (utf-16-le): b'\x12$s\xd7Z\xd1mK(\x02cd\xf6\xc0\xa9x'
   [+] Hex NT hash (utf-16-le): 122473d75ad16d4b28026364f6c0a978

[+] Step 3: Compute the MD4 hash of the nthash and the username
   [+] Raw DCC1 hash: b'H2,HIJAs\x0e\x1a?rV\xd9\x198'

[+] Step 4: We have the final DCC hash
   [+] Hex DCC1 hash: 48322c48494a41730e1a3f7256d91938
   [+] Hashcat format: 48322c48494a41730e1a3f7256d91938:Administrator
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
