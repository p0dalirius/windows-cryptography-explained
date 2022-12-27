# Lan Man (LM)


---

## Step by Step description

### 1. Setting the password in uppercase

The first step to create the LM hash is to set the password in uppercase:

![](./imgs/01.png)

### 2. Padding the password with null-bytes to a length 14 bytes

If the password is shorter than 14 bytes, we need to add padding null-bytes until it reaches a length of 14 bytes. If it is longer than 14 bytes, we just keep the first 14 bytes.

![](./imgs/02.png)

### 3. Splitting the encoded padded password

We then split the encoded padded password in 3 blocks of 7 bytes:

![](./imgs/03.png)

### 4. Add a parity bit after each block of 7 bits

![](./imgs/04.png)

### 4. DES encrypt the LM secret using K1 and K2

![](./imgs/05.png)

### 6. Concat CT1 and CT2 to form the final hash

Finally we concat the ciphertexts of steps 4 and 5 together to form the LM hash:

![](./imgs/06.png)

---

## Example

Using the attached [lm-hash-from-password.py](./lm-hash-from-password.py) python script, we can see the step by step values for computing the LM hash:

```
$ ./lm-hash-from-password.py -p 'Podalirius!'
[+] Raw password: b'Podalirius!'
[+] Upper raw password: b'PODALIRIUS!\x00\x00\x00'
[+] Message part 1: 504f44414c4952 | b'PODALIR'
  | parity_adjust(K1) = 5126d089156225a4
  | CT1 = d81491a2cc09ff01
[+] Message part 2: 49555321000000 | b'IUS!\x00\x00\x00'
  | parity_adjust(K2) = 49ab546410010101
  | CT2 = ea2ad910bb3f2a2a
[+] Raw LM hash: b'\xd8\x14\x91\xa2\xcc\t\xff\x01\xea*\xd9\x10\xbb?**'
[+] LM hash: d81491a2cc09ff01ea2ad910bb3f2a2a
```

## References
