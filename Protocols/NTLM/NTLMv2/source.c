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

Define LMOWFv2(Passwd, User, UserDom) as
    NTOWFv2(
        Passwd,
        User,
        UserDom
    )
EndDefine

Set ResponseKeyNT to NTOWFv2(Passwd, User, UserDom)
Set ResponseKeyLM to LMOWFv2(Passwd, User, UserDom)

Define ComputeResponse(NegFlg, ResponseKeyNT, ResponseKeyLM, CHALLENGE_MESSAGE.ServerChallenge, ClientChallenge, Time, ServerName) As
    If (User is set to "" && Passwd is set to "")
        -- Special case for anonymous authentication
        Set NtChallengeResponseLen to 0
        Set NtChallengeResponseMaxLen to 0
        Set NtChallengeResponseBufferOffset to 0
        Set LmChallengeResponse to Z(1)
    Else
        Set temp to ConcatenationOf(
            Responserversion,
            HiResponserversion,
            Z(6),
            Time,
            ClientChallenge,
            Z(4),
            ServerName,
            Z(4)
        )
        Set NTProofStr to HMAC_MD5(
            ResponseKeyNT,
            ConcatenationOf(
                CHALLENGE_MESSAGE.ServerChallenge,
                temp
            )
        )
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