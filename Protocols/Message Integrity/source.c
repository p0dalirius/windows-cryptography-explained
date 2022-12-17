-- Input:
-- SigningKey - The key used to sign the message.
-- Message - The message being sent between the client and server.
-- SeqNum - Defined in section 3.1.1.
-- Handle - The handle to a key state structure corresponding to
-- the current state of the SealingKey
--
-- Output: Signed message
-- Functions used:
-- ConcatenationOf() - Defined in Section 6.
-- MAC() - Defined in sections 3.4.4.1 and 3.4.4.2.
Define SIGN(Handle, SigningKey, SeqNum, Message) as
    ConcatenationOf(
        Message,
        MAC(
            Handle,
            SigningKey,
            SeqNum,
            Message
        )
    )
EndDefine