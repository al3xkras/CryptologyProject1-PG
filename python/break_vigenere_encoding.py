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
    def checkEveryNthSymbolMatchesModulo(Plaintext, Ciphertext, n, shift):
        assert len(Plaintext) == len(Ciphertext)
        delta = None
        for i in range(shift, len(Plaintext), n):
            d = ord(Plaintext[i]) - ord(Ciphertext[i])

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

    def __init__(self, Ciphertext):
        self.ciphertext = Ciphertext
        pass

    def deduceKeyWithUnsecureMessage(self, startsWith):
        return KnownPlainText([startsWith], [self.ciphertext[:len(startsWith)]]).deduceKey()

    def deduceKey(self):
        raise Exception(
            "It is impossible to deduce the key given only ciphertext (additional assumptions are required)")

    def deducePlainText(self):
        Key = self.deduceKey()

    def deducePlainTextWithUnsecureMessage(self, startsWith):
        Key = self.deduceKeyWithUnsecureMessage(startsWith)
        return VigenereEncoding(Key).decodeString(self.ciphertext)

    def modifyMessage(self):
        Key = self.deduceKey()

    def modifyUnsecureMessage(self, startsWith):
        _plaintext = self.deducePlainTextWithUnsecureMessage(startsWith)
        Key = self.deduceKeyWithUnsecureMessage(startsWith)
        _plaintext += "whoami"
        return VigenereEncoding(Key).encodeString(_plaintext).lower()


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
        return self.deduceKey()

    def deduceKey(self):
        iterKeyLength = 0
        maxLen = max(len(x) for x in self.plaintexts)

        while iterKeyLength <= maxLen:
            iterKeyLength += 1
            matched = True
            keyGlobal = None
            for i in range(len(self.plaintexts)):
                plain = self.plaintexts[i]
                cipher = self.ciphertexts[i]
                Key = ""
                for shift in range(iterKeyLength):
                    matched, delta = CipherUtils.checkEveryNthSymbolMatchesModulo(
                        plain, cipher, iterKeyLength, shift)
                    if not matched:
                        break
                    Key += chr(ord('a') + delta % 26)
                if not matched:
                    break
                if keyGlobal is None:
                    keyGlobal = Key
                    continue
                elif Key != keyGlobal:
                    raise Exception("invalid state")
                keyGlobal = Key
            if matched:
                return keyGlobal

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
        raise Exception("The solution is obvious after the key is found")

    def modifyMessage(self):
        raise Exception("The solution is obvious after the key is found")


class ChosenPlainText:
    """
    Ewa knows that a given ciphertext is encoded
        using the Vigenere encoding.
    Ewa has unlimited access to the encoder
    """

    def __init__(self, encoder, Plaintext):
        self.encoder = encoder
        self.plaintext = Plaintext

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

    def __init__(self, decoder, Ciphertext):
        self.decoder = decoder
        self.ciphertext = Ciphertext

    def deduceKeyWithUnsecureMessage(self):
        return self.deduceKey()

    def deduceKeyLength(self):
        text = "a" * len(self.ciphertext)
        textDecoded = self.decoder.decodeString(text)
        return CipherUtils.shortestCyclicSubstringLen(textDecoded)

    def deduceKey(self):
        key_length = self.deduceKeyLength()
        decoded = self.decoder.decodeString("a" * key_length)
        alphabet = [chr(x) for x in range(ord('a'), ord('z') + 1)]
        alpha = dict((alphabet[i], i) for i in range(len(alphabet)))
        return "".join(alphabet[(-alpha[x]) % len(alphabet)] for x in decoded)

    def deducePlainText(self):
        return self.decoder.decodeString(self.ciphertext)

    def modifyMessage(self):
        raise Exception("the solution is obvious.")


if __name__ == '__main__':
    action = "test1"
    if action == "test1":
        key = "master"
        encoding = VigenereEncoding(key)
        plaintext = "thesolutionisobvious"
        ciphertext = encoding.encodeString(plaintext).lower()
        test1 = CiphertextOnly(ciphertext)

        print(test1.deducePlainTextWithUnsecureMessage("thesolu"))
        print(test1.modifyUnsecureMessage("thesolu"))
        print(test1.deduceKeyWithUnsecureMessage("thesolu"))

    elif action == "test2":
        key = "avocado"
        encoding = VigenereEncoding(key)
        plaintexts = [
            "sometexttobedecodedblahblahblah", "happynewyear", "mydearfriends"
        ]
        ciphers = [encoding.encodeString(x).lower() for x in plaintexts]
        test2 = KnownPlainText(plaintexts, ciphers)
        keyLength = test2.deduceKeyLength()
        print(keyLength)
        print(test2.deduceKey())

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
