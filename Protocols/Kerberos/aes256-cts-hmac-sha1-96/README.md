# AES256-CTS-HMAC-SHA1-96

The `aes256-cts-hmac-sha1-96` is a password derivation function used in the Kerberos authentication protocol, enhancing security through the use of 256-bit AES encryption combined with HMAC (Hash-based Message Authentication Code) based on the SHA-1 hashing algorithm. This function produces a secure, fixed-size key derived from the user's password, ensuring compatibility with Kerberos' ticket-based authentication system and strong protection against unauthorized access.

The `aes256-cts-hmac-sha1-96` function is often preferred in high-security environments, as it provides a higher level of encryption than its 128-bit counterpart. This function creates a 256-bit AES key used for encrypting and validating authentication tokens in Kerberos, particularly within the ticket-granting process.

With stronger encryption than previous methods, such as DES and even `aes128-cts-hmac-sha1-96`, this function offers enhanced resistance to brute-force and dictionary attacks. However, its security is only as strong as the passwords used, making the choice of complex, unpredictable passwords critical for maintaining robust protection.

## 

## Example

```
$ ./kerberos-aes256-cts-hmac-sha1-96-key-from-password.py  -d ATHENA.MIT.EDU -u 'raeburn' -p 'password' -i 1
[+] Computing salt:
  | domain   = b'ATHENA.MIT.EDU'
  | username = b'raeburn'
  | salt = b'ATHENA.MIT.EDUraeburn'

[+] Computing PBKDF2-HMAC from password:
  | username = b'raeburn'
  | PBKDF2(salt+password) = cdedb5281bb2f801565a1122b25635150ad1f7a04bb9f3a333ecc0e2e1f70837

[+] Computing block 1
  | AES(key='cdedb5281bb2f801565a1122b25635150ad1f7a04bb9f3a333ecc0e2e1f70837').encrypt(KerberosConstant) = b"\xfei{R\xbc\r<\xe1D2\xba\x03j\x92\xe6[\xcbj\x07lQ\x91\xdc\x9f\x99\t\x9c[\x91\x9bwBz\xec=\xd55\x15\xff\xcb\x83'`\xb3y\x19\x1a\xaa"
  | CT1 = fe697b52bc0d3ce14432ba036a92e65bcb6a076c5191dc9f99099c5b919b77427aec3dd53515ffcb832760b379191aaa

[+] Computing block 2
  | AES(key='cdedb5281bb2f801565a1122b25635150ad1f7a04bb9f3a333ecc0e2e1f70837').encrypt(CT1) = b"\xbbR(\t\x90\xa2\xfa'\x889\x98\xd7*\xf3\x01a\x83\xf5\x81\xc6/\xf7\xd1>\xd1\xcd9\x8ef\xbc\xf2\xf7\xda\xb0\nR\xc5\x8e\xdf\x1a!\xe5%\x17W\xe3\x19b\xc5\x19\x90\xeb\x1a\xd5d\xf1\x95\x01z\xe2\\\x01\x02\xaa"
  | CT2 = bb52280990a2fa27883998d72af3016183f581c62ff7d13ed1cd398e66bcf2f7dab00a52c58edf1a21e5251757e31962c51990eb1ad564f195017ae25c0102aa

[+] Concatenating values:
  | CT1[:16] = fe697b52bc0d3ce14432ba036a92e65b
  | CT2[:16] = bb52280990a2fa27883998d72af30161
  | Kerberos aes256-cts-hmac-sha1-96 key for 'ATHENA.MIT.EDU\raeburn': fe697b52bc0d3ce14432ba036a92e65bbb52280990a2fa27883998d72af30161
```

## References
 - [RFC3961 - Encryption and Checksum Specifications for Kerberos 5](https://datatracker.ietf.org/doc/html/rfc3961)
 - [RFC3962 - Advanced Encryption Standard (AES) Encryption for Kerberos 5](https://datatracker.ietf.org/doc/html/rfc3962)


 