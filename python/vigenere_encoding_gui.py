import tkinter as tk
from functools import wraps

gui = None

def letter_encode_decorator(function):
    global gui
    keyLetter = None
    encoded = None
    textLetter = None

    def wrapper(self, *args, **kwargs):
        nonlocal keyLetter, encoded, textLetter
        keyLetter = kwargs["keyLetter"] if "keyLetter" in kwargs else args[1]
        textLetter = kwargs["textLetter"] if "textLetter" in kwargs else args[0]
        encoded = function(self, *args, **kwargs)
        try:
            gui.drawNextEncodedLetter(keyLetter, textLetter, encoded)
        except:
            print("failed to visualize next encoded letter: ", keyLetter, textLetter, encoded)
        return encoded
    return wrapper

def letter_decode_decorator(function, *args):
    global gui
    keyLetter = None
    decoded = None
    encodedLetter = None
    def wrapper(self, *args, **kwargs):
        nonlocal keyLetter, decoded, encodedLetter
        keyLetter = kwargs["keyLetter"] if "keyLetter" in kwargs else args[1]
        encodedLetter = kwargs["encodedLetter"] if "encodedLetter" in kwargs else args[0]
        decoded = function(self, *args, **kwargs)
        try:
            gui.drawNextDecodedLetter(keyLetter, encodedLetter, decoded)
        except:
            print("failed to visualize next decoded letter: ", keyLetter, encodedLetter, decoded)
        return decoded
    return wrapper

class VigenereEncodingGUI:
    def __init__(self, screen):
        self.screen = screen


class BreakVigenereEncodingGUI:
    def __init__(self, screen):
        self.screen = screen


