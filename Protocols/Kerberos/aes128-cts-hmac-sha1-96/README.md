# AES128-CTS-HMAC-SHA1-96

The `aes128-cts-hmac-sha1-96` is a password derivation function used in the Kerberos authentication protocol, which is a widely adopted network authentication system. This function combines AES (Advanced Encryption Standard) encryption with HMAC (Hash-based Message Authentication Code) based on the SHA-1 hashing algorithm, producing a secure hash for password verification. It derives a fixed-size key from the user's password input, ensuring both security and compatibility with Kerberos' ticket-based authentication.

The `aes128-cts-hmac-sha1-96` function is commonly used in Kerberos authentication protocols, particularly in environments requiring secure and efficient authentication mechanisms. This derivation method creates a 128-bit AES encryption key, which is used to encrypt and validate authentication tokens within Kerberos' ticket-granting process.

Compared to older encryption mechanisms, such as DES, the `aes128-cts-hmac-sha1-96` is considerably more secure. It can handle long and complex passwords, enhancing resistance to brute-force and dictionary attacks. However, like all cryptographic functions, its effectiveness relies on using strong, unpredictable passwords to ensure robust security.

## 

## Example

```
$ ./kerberos-aes128-cts-hmac-sha1-96-key-from-password.py -d ATHENA.MIT.EDU -u 'raeburn' -p 'password' -i 1
[+] Computing salt:
  | domain   = b'ATHENA.MIT.EDU'
  | username = b'raeburn'
  | salt = b'ATHENA.MIT.EDUraeburn'

[+] Computing PBKDF2-HMAC from password:
  | username = b'raeburn'
  | PBKDF2(salt+password) = cdedb5281bb2f801565a1122b2563515

[+] Encrypting constant with AES:
  | AES(key='cdedb5281bb2f801565a1122b2563515').encrypt(KerberosConstant) = b'B&<n\x89\xf4\xfc(\xb8\xdfh\xee\ty\x9f\x15\x9cV\xd9>\xc5\xda\xb3$\xb6\x16\xd8W\xd0\x11\xbe\xecr\x8ayYv\x82\xd4\xe9u\xfd\xbcTP>\x7f\xbe'
  | CT1 = 42263c6e89f4fc28b8df68ee09799f159c56d93ec5dab324b616d857d011beec728a79597682d4e975fdbc54503e7fbe

[+] Concatenating values:
  | CT1[:16] = 42263c6e89f4fc28b8df68ee09799f15
  | Kerberos aes128-cts-hmac-sha1-96 key for 'ATHENA.MIT.EDU\raeburn': 42263c6e89f4fc28b8df68ee09799f15
```

## References
 - [RFC3961 - Encryption and Checksum Specifications for Kerberos 5](https://datatracker.ietf.org/doc/html/rfc3961)
 - [RFC3962 - Advanced Encryption Standard (AES) Encryption for Kerberos 5](https://datatracker.ietf.org/doc/html/rfc3962)

