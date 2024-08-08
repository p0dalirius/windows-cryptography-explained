# NTLMv2 Authentication Protocol

NTLMv2 (NT LAN Manager version 2) is an authentication protocol used in Windows environments to authenticate users and secure access to resources. It is an improvement over NTLMv1, offering enhanced security features, including stronger encryption and better resistance to attacks.

NTLMv2 involves creating an HMAC-MD5 hash of the NT hash of the user's password, along with other elements like the server challenge, client challenge, timestamp, and other session-related data. This hash, known as the NTLMv2 response, is used for authentication.

> [!IMPORTANT]
> NTLMv2 provides better security than NTLMv1, but it is still vulnerable to certain attacks, such as pass-the-hash, and lacks mutual authentication. Use of NTLMv2 is generally recommended over NTLMv1, though more secure protocols like Kerberos are preferred.

---

## Definition

Source: [https://learn.microsoft.com/en-us/openspecs/windows_protocols/ms-nlmp/5e550938-91d4-459f-b67d-75d70009e3f3](https://learn.microsoft.com/en-us/openspecs/windows_protocols/ms-nlmp/5e550938-91d4-459f-b67d-75d70009e3f3?wt.mc_id=SEC-MVP-5005286)

```python
# 
Define NTOWFv2(Passwd, User, UserDom) as
  HMAC_MD5( 
    MD4(
      UNICODE(Passwd)
    ),
    UNICODE(
      ConcatenationOf(
        Uppercase(User), 
        UserDom
      )
    )
  )
EndDefine

# 
Define LMOWFv2(Passwd, User, UserDom) as NTOWFv2(Passwd, User, UserDom)
EndDefine

Set ResponseKeyNT to NTOWFv2(Passwd, User, UserDom)
Set ResponseKeyLM to LMOWFv2(Passwd, User, UserDom)

# Function to compute the NTLMv2 challenge
Define ComputeResponse(NegFlg, ResponseKeyNT, ResponseKeyLM, CHALLENGE_MESSAGE.ServerChallenge, ClientChallenge, Time, ServerName) as
  If (User is set to "" && Passwd is set to "")
    # Special case for anonymous authentication
    Set NtChallengeResponseLen to 0
    Set NtChallengeResponseMaxLen to 0
    Set NtChallengeResponseBufferOffset to 0
    Set LmChallengeResponse to Z(1)
  Else
    Set temp to ConcatenationOf(Responserversion, HiResponserversion, Z(6), Time, ClientChallenge, Z(4), ServerName, Z(4))
    Set NTProofStr to HMAC_MD5(ResponseKeyNT, ConcatenationOf(CHALLENGE_MESSAGE.ServerChallenge,temp))
    Set NtChallengeResponse to ConcatenationOf(NTProofStr, temp)
    Set LmChallengeResponse to ConcatenationOf(
      HMAC_MD5(
        ResponseKeyLM,
        ConcatenationOf(
          CHALLENGE_MESSAGE.ServerChallenge,
          ClientChallenge
        )
      ),
      ClientChallenge
    )
  EndIf
  Set SessionBaseKey to HMAC_MD5(ResponseKeyNT, NTProofStr)
EndDefine
```

