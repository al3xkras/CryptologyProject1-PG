from vigenere_encoding_gui import letter_encode_decorator, letter_decode_decorator,string_encoder,string_decoder, mainloop_handler

class VigenereEncoding:
    """
    A python implementation of the Vigenere Cipher

    The cipher definition available at the link:
    https://enauczanie.pg.edu.pl/moodle/pluginfile.php/2191089/mod_resource/content/8/Kryptologia%20lab06.%20Szyfry%20podstawieniowe%20polialfabetyczne.pdf

    Which is equivalent to the definition on Wikipedia:
    https://en.wikipedia.org/wiki/Vigen%C3%A8re_cipher
    """
    alphabet = [chr(x) for x in range(ord('a'), ord('z') + 1)]

    def __init__(self, key: str, alphabet=None):
        self.key = key
        if alphabet is not None:
            self.alphabet = alphabet
        else:
            self.alphabet = VigenereEncoding.alphabet
        self.alpha = dict((self.alphabet[i], i) for i in range(len(self.alphabet)))

    @letter_encode_decorator
    def encodeLetter(self, textLetter, keyLetter):
        textLetter = textLetter[0].lower()
        keyLetter = keyLetter[0].lower()
        return self.alphabet[(self.alpha[textLetter] + self.alpha[keyLetter]) % len(self.alpha)]

    @letter_decode_decorator
    def decodeLetter(self, encodedLetter, keyLetter):
        encodedLetter = encodedLetter[0].lower()
        keyLetter = keyLetter[0].lower()
        return self.alphabet[(self.alpha[encodedLetter] - self.alpha[keyLetter]) % len(self.alpha)]

    @string_encoder
    def encodeString(self, string):
        i = 0
        mod = len(self.key)
        encoded = ""
        for s in string:
            encoded += self.encodeLetter(s, self.key[i])
            i = (i + 1) % mod
        return encoded.upper()

    @string_decoder

    def decodeString(self, string):
        i = 0
        mod = len(self.key)
        encoded = ""
        for s in string:
            encoded += self.decodeLetter(s, self.key[i])
            i = (i + 1) % mod
        return encoded



if __name__ == '__main__':
    @mainloop_handler
    def main():
        v = VigenereEncoding("lemon")
        enc = v.encodeString("ata")
        enc = v.encodeString("cka")
        print(enc)
        dec = v.decodeString(enc)
        print(dec)
    main()