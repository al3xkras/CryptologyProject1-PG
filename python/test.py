from vigenere_encoding_gui import VigenereEncodingGUI,mainloop_handler
import vigenere_encoding_gui
from vigenere_encoding import VigenereEncoding
from break_vigenere_encoding import *

import break_vigenere_encoding
@mainloop_handler
def main_break_enco_methods():
    action = "notest"
    if action == "notest":
        key = "master"
        break_vigenere_encoding.enco.key=key
        encoding = break_vigenere_encoding.enco

    elif action == "test1":
        key = "master"
        break_vigenere_encoding.enco.key=key
        encoding = break_vigenere_encoding.enco
        plaintext = "thesolutionisobvious"
        ciphertext = encoding.encodeString(plaintext).lower()
        test1 = CiphertextOnly(ciphertext)

        print(test1.deducePlainTextWithUnsecureMessage("thesolu"))
        print(test1.modifyUnsecureMessage("thesolu"))
        print(test1.deduceKeyWithUnsecureMessage("thesolu"))

    elif action == "test2":
        key = "avocado"
        break_vigenere_encoding.enco.key=key
        encoding = break_vigenere_encoding.enco
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
        break_vigenere_encoding.enco.key=key
        encoding = break_vigenere_encoding.enco
        test3 = ChosenPlainText(encoding, "ninetyninebugsfixed")
        keyLength = test3.deduceKeyLength()
        print(keyLength)
        print(test3.deduceKey())

    elif action == "test4":
        key = "lemon"
        break_vigenere_encoding.enco.key=key
        encoding = break_vigenere_encoding.enco
        test3 = ChosenCiphertext(encoding, encoding.encodeString("attackatdawn"))
        keyLength = test3.deduceKeyLength()
        print(keyLength)
        print(test3.deduceKey())

if __name__ == '__main__':
    from vigenere_encoding import VigenereEncoding
    enc=VigenereEncoding(key="kiwi")
    break_vigenere_encoding.enco=enc
    vigenere_encoding_gui.gui.enc=enc
    main_break_enco_methods()
