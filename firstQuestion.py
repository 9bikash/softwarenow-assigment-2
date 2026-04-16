#question 1

import string

#stores alphabets both lower and upper case 
LOWER1 = "abcdefghijklm"
LOWER2 = "nopqrstuvwxyz"
UPPER1 = "ABCDEFGHIJKLM"
UPPER2 = "NOPQRSTUVWXYZ"


def shift(c, amount, alphabet):
    idx = alphabet.index(c)
    return alphabet[(idx + amount) % len(alphabet)]


def encrypt_char(c, s1, s2):
    if c in LOWER1:
        return shift(c, s1 * s2, LOWER1)
    elif c in LOWER2:
        return shift(c, -(s1 + s2), LOWER2)
    elif c in UPPER1:
        return shift(c, -s1, UPPER1)
    elif c in UPPER2:
        return shift(c, s2 * s2, UPPER2)
    return c


def decrypt_char(c, s1, s2):
    '''
    Rules for decryption:
    - Lowercase from a to m: shift forward by s1 * s2
    - Lowercase from n to z: shift forward by s1 + s2
    - Uppercase from A to M: shift forward by s1
    - Uppercase from N to Z: shift backward by s2^2
    - Remaining other characters are unchanged
    '''
    if c in LOWER1:
        return shift(c, -(s1 * s2), LOWER1)
    elif c in LOWER2:
        return shift(c, (s1 + s2), LOWER2)
    elif c in UPPER1:
        return shift(c, s1, UPPER1)
    elif c in UPPER2:
        return shift(c, -(s2 * s2), UPPER2)
    return c


def encrypt_file(s1, s2):
    with open("raw_text.txt", "r", encoding="utf-8") as f:
        text = f.read()

    encrypted = "".join(encrypt_char(c, s1, s2) for c in text)

    with open("encrypted_text.txt", "w", encoding="utf-8") as f:
        f.write(encrypted)


def decrypt_file(s1, s2):
    #reads the text from encrypted_text.txt and decrypts it using the decrypt_char function, then writes the decrypted text to decrypted_text.txt   
    with open("encrypted_text.txt", "r", encoding="utf-8") as f:
        text = f.read()

    decrypted = "".join(decrypt_char(c, s1, s2) for c in text)

    with open("decrypted_text.txt", "w", encoding="utf-8") as f:
        f.write(decrypted)


def verify():
    #compares the original text from raw_text.txt with the decrypted text from decrypted_text.txt to check if they match. 
    with open("raw_text.txt", "r", encoding="utf-8") as f1:
        original = f1.read()

    with open("decrypted_text.txt", "r", encoding="utf-8") as f2:
        decrypted = f2.read()

    if original == decrypted:
        print("MATCH — Decryption successful.")
    else:
        print("NO MATCH — Something is wrong.")


def main():
    #main function that asks user to input two shifts values.
    s1 = int(input("shift1: "))
    s2 = int(input("shift2: "))

    encrypt_file(s1, s2)
    decrypt_file(s1, s2)
    verify()


if __name__ == "__main__":
    main()