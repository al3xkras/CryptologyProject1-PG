from vigenere_encoding_gui import VigenereEncodingGUI,mainloop_handler
import vigenere_encoding_gui
from vigenere_encoding import VigenereEncoding

if __name__ == '__main__':
    @mainloop_handler
    def main():
        enc=VigenereEncoding("abc")
        vigenere_encoding_gui.gui.enc=enc
    main()
