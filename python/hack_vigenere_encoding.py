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

    def deduceKeyWithUnsecureMessage(self):
        pass

    def deduceKey(self):
        pass

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

    def deduceKeyWithUnsecureMessage(self):
        pass

    def deduceKey(self):
        pass

    def deducePlainText(self):
        pass

    def modifyMessage(self):
        pass


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

    key = "lemon"
    encoding = VigenereEncoding(key)
    test4 = ChosenCiphertext(encoding, encoding.encodeString("attackatdawn"))
    length = test4.deduceKeyLength()
    print(length)
    print(test4.deduceKey())
