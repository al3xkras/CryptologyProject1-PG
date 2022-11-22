from vigenere_encoding import VigenereEncoding

hacking_types = [
    "key_deduction",
    "plaintext_deduction",
    "plaintext_modification"
]


class CipherUtils:
    @staticmethod
    def checkEveryNthSymbolEq(string, symbol, n, shift):
        for i in range(shift, len(string), n):
            if string[i] != symbol:
                return False
        return True

    @staticmethod
    def checkEveryNthSymbolMatchesModulo(plaintext, ciphertext, n, shift):
        assert len(plaintext) == len(ciphertext)
        delta = None
        for i in range(shift, len(plaintext), n):
            d = ord(plaintext[i]) - ord(ciphertext[i])

            if delta is None:
                delta = d
                continue

            if d != delta and (abs(d) + abs(delta)) % 26 != 0:
                return False, None
        return True, delta

    @staticmethod
    def shortestCyclicSubstringLen(string):
        cycleLen = 1
        while cycleLen < len(string):
            eq = None
            i = 0
            for symbol in string[:cycleLen]:
                eq = CipherUtils.checkEveryNthSymbolEq(string, symbol, cycleLen, shift=i)
                i += 1
                if not eq:
                    break
            if eq:
                return cycleLen
            cycleLen += 1
        return cycleLen


class CiphertextOnly:
    """
    Ewa knows that a given ciphertext is encoded
    using the Vigenere encoding.
    Another assumption is that the plain text is
        a message in a given language.
    The message is secure (i.e.
        Does not start or end with predictable phrases like
        "Dear <name>" "Sincerely yours, <name>" etc
    """

    def __init__(self):
        pass

    def deduceKeyWithUnsecureMessage(self):
        pass

    def deduceKey(self):
        pass

    def deducePlainText(self):
        pass

    def modifyMessage(self):
        pass


class KnownPlainText:
    """
    Ewa knows that a given ciphertext is encoded
        using the Vigenere encoding.
    Ewa has access to a set of ciphertext-plaintext pairs
        encoded with the same algorithm
    """

    def __init__(self, ciphertext_samples, plaintext_samples):
        self.ciphertexts = ciphertext_samples
        self.plaintexts = plaintext_samples

    def deduceKeyWithUnsecureMessage(self):
        pass

    def deduceKey(self):
        pass

    def deduceKeyLength(self):
        iterKeyLength = 0
        maxLen = max(len(x) for x in self.plaintexts)

        while iterKeyLength <= maxLen:
            iterKeyLength += 1
            matched = True
            for i in range(len(self.plaintexts)):
                plain = self.plaintexts[i]
                cipher = self.ciphertexts[i]
                for shift in range(iterKeyLength):
                    matched, delta = CipherUtils.checkEveryNthSymbolMatchesModulo(
                        plain, cipher, iterKeyLength, shift)
                    if not matched:
                        break
                if not matched:
                    break
            if matched:
                return iterKeyLength
        raise Exception("Failed to deduce the key length.")

    def deducePlainText(self):
        pass

    def modifyMessage(self):
        pass


class ChosenPlainText:
    """
    Ewa knows that a given ciphertext is encoded
        using the Vigenere encoding.
    Ewa has unlimited access to the encoder
    """

    def __init__(self, encoder, plaintext):
        self.encoder = encoder
        self.plaintext = plaintext

    def deduceKeyWithUnsecureMessage(self):
        return self.deduceKey()

    def deduceKey(self):
        keyLen = self.deduceKeyLength()
        decoded = self.encoder.encodeString("a" * keyLen)
        return decoded

    def deduceKeyLength(self):
        text = "a" * len(self.plaintext)
        textEncoded = self.encoder.encodeString(text)
        return CipherUtils.shortestCyclicSubstringLen(textEncoded)

    def deducePlainText(self):
        return self.plaintext

    def modifyMessage(self):
        raise Exception("This action does not require breaking the cipher")


class ChosenCiphertext:
    """
    Ewa knows that a given ciphertext is encoded
        using the Vigenere encoding.
    Ewa has unlimited access to the decoder
    """

    def __init__(self, decoder, ciphertext):
        self.decoder = decoder
        self.ciphertext = ciphertext

    def deduceKeyWithUnsecureMessage(self):
        return self.deduceKey()

    def deduceKeyLength(self):
        text = "a" * len(self.ciphertext)
        textDecoded = self.decoder.decodeString(text)
        return CipherUtils.shortestCyclicSubstringLen(textDecoded)

    def deduceKey(self):
        keyLength = self.deduceKeyLength()
        decoded = self.decoder.decodeString("a" * keyLength)
        alphabet = [chr(x) for x in range(ord('a'), ord('z') + 1)]
        alpha = dict((alphabet[i], i) for i in range(len(alphabet)))
        return "".join(alphabet[(-alpha[x]) % len(alphabet)] for x in decoded)

    def deducePlainText(self):
        return self.decoder.decodeString(self.ciphertext)

    def modifyMessage(self):
        raise Exception("the solution is obvious.")


if __name__ == '__main__':
    action = "test2"
    if action == "test2":
        key = "avocado"
        encoding = VigenereEncoding(key)
        plaintexts = [
            "sometexttobedecodedblahblahblah", "happynewyear", "mydearfriends"
        ]
        ciphers = [encoding.encodeString(x).lower() for x in plaintexts]
        print(ciphers)
        test2 = KnownPlainText(plaintexts, ciphers)
        keyLength = test2.deduceKeyLength()
        print(keyLength)

    elif action == "test3":
        key = "banana"
        encoding = VigenereEncoding(key)
        test3 = ChosenPlainText(encoding, "ninetyninebugsfixed")
        keyLength = test3.deduceKeyLength()
        print(keyLength)
        print(test3.deduceKey())
    elif action == "test4":
        key = "lemon"
        encoding = VigenereEncoding(key)
        test3 = ChosenCiphertext(encoding, encoding.encodeString("attackatdawn"))
        keyLength = test3.deduceKeyLength()
        print(keyLength)
        print(test3.deduceKey())
