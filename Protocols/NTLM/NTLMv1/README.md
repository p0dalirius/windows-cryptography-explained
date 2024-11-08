# NTLMv1 Authentication Protocol

NTLMv1 (NT LAN Manager version 1) is an authentication protocol used in Windows environments to authenticate users and provide secure access to resources. It involves computing the NT hash of the user's password and using it to generate an NTLMv1 hash for authentication.

NTLMv1 hash is computed by performing DES encryption on three blocks of data derived from the NT hash and server challenge. The resulting hash is used for authentication purposes.

> [!IMPORTANT]
> NTLMv1 is considered to be a weak authentication protocol due to vulnerabilities such as pass-the-hash attacks and lack of mutual authentication.

---

## Definition

Source: [https://learn.microsoft.com/en-us/openspecs/windows_protocols/ms-nlmp/464551a8-9fc4-428e-b3d3-bc5bfb2e73a5](https://learn.microsoft.com/en-us/openspecs/windows_protocols/ms-nlmp/464551a8-9fc4-428e-b3d3-bc5bfb2e73a5?wt.mc_id=SEC-MVP-5005286)

```python
# Function to compute the NT One Way Function 
Define NTOWFv1(Passwd, User, UserDom) as
 MD4(UNICODE(Passwd))
EndDefine

# Function to compute the LanMan One Way Function 
Define LMOWFv1(Passwd, User, UserDom) as
  ConcatenationOf(
    DES(UpperCase(Passwd)[0..6], "KGS!@#$%"),
    DES(UpperCase(Passwd)[7..13], "KGS!@#$%")
  )
EndDefine

Set ResponseKeyNT to NTOWFv1(Passwd, User, UserDom)
Set ResponseKeyLM to LMOWFv1(Passwd, User, UserDom)

# Function to compute the NTLMv1 challenge
Define ComputeResponse(NegFlg, ResponseKeyNT, ResponseKeyLM, CHALLENGE_MESSAGE.ServerChallenge, ClientChallenge, Time, ServerName) as
  If (User is set to "" AND Passwd is set to "")
    # Special case for anonymous authentication
    Set NtChallengeResponseLen to 0
    Set NtChallengeResponseMaxLen to 0
    Set NtChallengeResponseBufferOffset to 0
    Set LmChallengeResponse to Z(1)
  ElseIf
    If (NTLMSSP_NEGOTIATE_EXTENDED_SESSIONSECURITY flag is set in NegFlg) 
       Set NtChallengeResponse to
        DESL(
          ResponseKeyNT,
          MD5(ConcatenationOf(CHALLENGE_MESSAGE.ServerChallenge, ClientChallenge))[0..7]
        )
       Set LmChallengeResponse to ConcatenationOf{ClientChallenge, Z(16)}
    Else 
       Set NtChallengeResponse to DESL(ResponseKeyNT, CHALLENGE_MESSAGE.ServerChallenge)
       If (NoLMResponseNTLMv1 is TRUE)
           Set LmChallengeResponse to NtChallengeResponse
       Else 
           Set LmChallengeResponse to DESL(ResponseKeyLM, CHALLENGE_MESSAGE.ServerChallenge)
       EndIf
    EndIf
EndIf

Set SessionBaseKey to MD4(NTOWF)
```

The `UNICODE` function here is refering to a `UTF-16-LE` (Little Endian) encoding.

---

---

## Step by Step description

### 1. Compute the NT hash of the password


## Example

```
$ ./ntlmv1-from-password.py -p 'Podalirius!'
[+] Server challenge: b'\x11"3DUfw\x88' | hex: 1122334455667788
[+] Raw password: b'P\x00o\x00d\x00a\x00l\x00i\x00r\x00i\x00u\x00s\x00!\x00'
[+] NT hash: 122473d75ad16d4b28026364f6c0a978
[+] NTLM-Hash | 5-bytes-0: 122473d75ad16d4b28026364f6c0a9780000000000
[+] Computing block 1
  | K1 = b'\x12$s\xd7Z\xd1m' | hex: 122473d75ad16d
  | parity_adjust(K1) = 13131c7a75d645da
  | DES(key='122473d75ad16d').encrypt('1122334455667788') = b'\x81\x10w\x9aGQ{\x1e'
  | CT1 = 8110779a47517b1e
[+] Computing block 2
  | K2 = b'K(\x02cd\xf6\xc0' | hex: 4b28026364f6c0
  | parity_adjust(K2) = 4a94014c3726da80
  | DES(key='4b28026364f6c0').encrypt('1122334455667788') = b'k\xd6\x861{\xd8\xbc9'
  | CT2 = 6bd686317bd8bc39
[+] Computing block 3
  | K3 = b'\xa9x\x00\x00\x00\x00\x00' | hex: a9780000000000
  | parity_adjust(K3) = a8bc010101010101
  | DES(key='a9780000000000').encrypt('1122334455667788') = b'Z\x07\xa6@\xad\x9e>p'
  | CT3 = 5a07a640ad9e3e70
[+] CT1 + CT2 + CT3: 8110779A47517B1E6BD686317BD8BC395A07A640AD9E3E70

[+] NTLMv1 hash: 8110779A47517B1E6BD686317BD8BC395A07A640AD9E3E70
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

 - https://learn.microsoft.com/en-us/archive/blogs/openspecification/ntlm-keys-and-sundry-stuff
 - https://www.praetorian.com/blog/ntlmv1-vs-ntlmv2/
