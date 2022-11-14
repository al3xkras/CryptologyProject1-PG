from vigenere_encoding import VigenereEncoding

hacking_types = [
    "key_deduction",
    "plaintext_deduction",
    "plaintext_modification"
]


class CipherUtils:
    @staticmethod
    def checkEveryNthSymbolEq(string, symbol, n):
        assert len(symbol == 1)
        assert round(len(string) / n, 3) is int
        for i in range(0, len(string) + n, n):
            if string[i] != symbol:
                return False
        return True

    @staticmethod
    def shortestCyclicSubstringLen(string):
        cycleLen = 1
        while cycleLen < len(string):
            eq = None
            for symbol in string[:cycleLen]:
                eq = CipherUtils.checkEveryNthSymbolEq(string, symbol, cycleLen)
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

    def modifyPlainText(self):
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

    def modifyPlainText(self):
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

    def modifyPlainText(self):
        pass


class ChosenCiphertext:
    """
    Ewa knows that a given ciphertext is encoded
        using the Vigenere encoding.
    Ewa has unlimited access to the decoder
    """

    def __init__(self, decoder):
        self.decoder = decoder
        self.ciphertext = \
            """abcd"""

    def deduceKeyWithUnsecureMessage(self):
        pass

    def deduceKeyLength(self):
        text = "a" * len(self.ciphertext)
        textDecoded = self.decoder.decodeString(text)
        return CipherUtils.shortestCyclicSubstringLen(textDecoded)

    def deduceKey(self):
        keyLength = self.deduceKeyLength()
        return self.decoder.decodeString("A" * keyLength)

    def deducePlainText(self):
        return self.decoder.decodeString(self.ciphertext)

    def modifyPlainText(self):
        raise Exception("the solution is obvious.")


if __name__ == '__main__':
    key = ""
    encoder = VigenereEncoding(key)
