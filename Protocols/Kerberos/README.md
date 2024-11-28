# Kerberos

## Encryption types

| Kerberos Algorithm                  | Encryption Type Value  |
|-------------------------------------|----------------------------|
| [`des-cbc-crc`](./des-cbc-crc/)     | [`1`](./aes128-cts-hmac-sha1-96/) |
| [`des-cbc-md5`](./des-cbc-md5/)     | [`2`](./aes128-cts-hmac-sha1-96/) |
| [`rc4-hmac`](./rc4-hmac/)           | [`4`](./aes128-cts-hmac-sha1-96/) |
| [`aes128-cts-hmac-sha1-96`](./aes128-cts-hmac-sha1-96/) | [`8`](./aes128-cts-hmac-sha1-96/) |
| [`aes256-cts-hmac-sha1-96`](./aes256-cts-hmac-sha1-96/) | [`24`](./aes128-cts-hmac-sha1-96/) |
| future encryption types (reserved)  | `32`, `64`, etc. |

## References
 - [https://techcommunity.microsoft.com/blog/coreinfrastructureandsecurityblog/decrypting-the-selection-of-supported-kerberos-encryption-types/1628797](https://techcommunity.microsoft.com/blog/coreinfrastructureandsecurityblog/decrypting-the-selection-of-supported-kerberos-encryption-types/1628797)