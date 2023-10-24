# Hash NT

The Hash NT is a password hashing algorithm used in Microsoft Windows operating systems. It is a cryptographic hash function that takes a user's password as input and produces a fixed-size hash value as output. The Hash NT is based on the MD4 algorithm and is used to store and verify user passwords ""securely"".

The Hash NT is widely used in Windows [authentication protocols](../../Protocols/), such as [NTLMv1](../../Protocols/NTLMv1/) and [NTLMv2](../../Protocols/NTLMv2/). It is used to generate the NT hash, which is a one-way transformation of the user's password. The NT hash is then used for various purposes, including password authentication and password cracking.

Unlike the [Lan Man (LM)](../Lan%20Man%20(LM)/) hash, which is considered weak and vulnerable, the Hash NT is more secure and can handle passwords of any length. It is not limited to 14 characters like the LM hash. However, it is still susceptible to brute-force and dictionary attacks if weak passwords are used.

---

## Step by Step computation

### 1. Encode password in UTF-16-LE



### 2. Compute MD4 of the encoded password



## Example

Using the attached [nt-hash-from-password.py](./nt-hash-from-password.py) python script, we can see the step by step values for computing the NT hash:

```
$ ./nt-hash-from-password.py -p 'Podalirius!' -v
[+] Raw password (utf-16-le): b'P\x00o\x00d\x00a\x00l\x00i\x00r\x00i\x00u\x00s\x00!\x00'
[+] Raw NT hash: b'\x12$s\xd7Z\xd1mK(\x02cd\xf6\xc0\xa9x'
[+] NT hash: 122473d75ad16d4b28026364f6c0a978
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
 - https://blog.gentilkiwi.com/securite/mscache-v2-dcc2-iteration
