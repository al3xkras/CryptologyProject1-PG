from unittest import TestCase
from vigenere_encoding import VigenereEncoding

class TestVigenereEncoding(TestCase):

    def test_encode_letter(self):
        key="chara"
        v = VigenereEncoding(key)
        letter1 = 'q'
        expected1 = chr(ord('a')+(ord('q')+ord('c')-2*ord('a'))%26)

        self.assertEqual(expected1,v.encodeLetter(letter1,key[0]))

        letter2 = 'm'
        expected2 = chr(ord('a')+(ord('m')-ord('a'))%26)

        self.assertEqual(expected2, v.encodeLetter(letter2, key[2]))

    def test_decode_letter(self):
        key = "sans"
        v = VigenereEncoding(key)
        letter1 = 'n'
        expected1 = chr(ord('a') + (ord('n') - ord('s')) % 26)

        self.assertEqual(expected1, v.decodeLetter(letter1, key[0]))

        letter2 = 'b'
        expected2 = chr(ord('a') + (ord('b') - ord('n')) % 26)

        self.assertEqual(expected2, v.decodeLetter(letter2, key[2]))

    def test_encode_string(self):
        v = VigenereEncoding("lemon")
        enc = v.encodeString("attackatdawn")
        self.assertEqual("LXFOPVEFRNHR",enc.upper())

    def test_decode_string(self):
        v = VigenereEncoding("lemon")
        dec = v.decodeString("LXFOPVEFRNHR")
        self.assertEqual("attackatdawn",dec.lower())
