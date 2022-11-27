import sys
import tkinter as tk
from functools import wraps
import threading
from time import sleep
class Symbol:
    width=30
    height=30
    font_size = 14
    offset=5
    indent=50
    def __init__(self, canvas:tk.Canvas, pos, symbol):
        self.canvas=canvas
        self.pos=pos
        self.symbol=symbol
        self.rect=None
        self.text=None
    def draw(self):
        x1=self.pos[0]
        x2=self.pos[0]+Symbol.width
        y1=self.pos[1]
        y2=self.pos[1]+Symbol.height
        self.rect=self.canvas.create_rectangle(x1,y1,x2,y2)
        self.text=self.canvas.create_text(x1+Symbol.width/2-Symbol.font_size/2+Symbol.offset,
                                          y1+Symbol.height/2-Symbol.font_size/2+Symbol.offset,
                                font=str(Symbol.font_size), text=self.symbol)
    def remove(self):
        del self.rect
        del self.text

    def drawNextTo(self, other):
        self.pos=(other.pos[0]+Symbol.width+Symbol.offset,other.pos[1])
        self.draw()


lock1=threading.Lock()
class VigenereEncodingGUI:
    w=500
    h=300
    scr_size="%sx%s"%(w,h)
    def __init__(self):
        self.screen = tk.Tk()
        self.screen.geometry(VigenereEncodingGUI.scr_size)
        self.text_input=None
        self.ciphertext_output=None
        self.button_encode=None
        self.button_decode=None
        self.gui_fragment=tk.Canvas(self.screen,width=500,height=300,background="green")
        self.gui_fragment.pack(fill="both",expand=True)
        self.last_symbol_encoded=[None,None,None]
        self.fragment_symbols=[]
        self.w=VigenereEncodingGUI.w
        self.h=VigenereEncodingGUI.h

    def resize(self,w,h):
        scr_size="%sx%s"%(w,h)
        self.screen.geometry(scr_size)
        self.w=w
        self.h=h

    def drawNextEncodedLetter(self,keyLetter, textLetter, encoded):
        self._drawNextEncoded(keyLetter, 1, offset=100)
        self._drawNextEncoded(textLetter, 0)
        self._drawNextEncoded(encoded, 2, offset=70)

    def _drawNextEncoded(self,letter,pos=0,offset=None):
        w=offset
        if offset is None:
            w=Symbol.offset
        if self.last_symbol_encoded[pos] is None:
            sym=Symbol(self.gui_fragment,(Symbol.offset,Symbol.offset+w*pos),
                       letter)
            self.fragment_symbols.append(sym)
            sym.draw()
            self.last_symbol_encoded[pos]=sym
        else:
            sym = Symbol(self.gui_fragment, (0,0),
                         letter)
            sym.drawNextTo(self.last_symbol_encoded[pos])
            self.last_symbol_encoded[pos]=sym

    def _clearFragment(self):
        for x in self.fragment_symbols:
            self.gui_fragment.delete("all")
        self.fragment_symbols=[]
        self.last_symbol_encoded=[None,None,None]


    def drawNextDecodedLetter(self,keyLetter, encodedLetter, decoded):
        pass
    def update(self):
        self.screen.update()

    def mainloop(self):
        self.screen.mainloop()

class BreakVigenereEncodingGUI:
    def __init__(self, screen):
        self.screen = screen


lock=threading.Lock()
gui=None
def initGui():
    global gui
    gui = VigenereEncodingGUI()
    lock.release()
    gui.mainloop()
thr = threading.Thread(target=initGui)
thr.start()
lock.acquire()

def letter_encode_decorator(function):
    global gui
    keyLetter = None
    encoded = None
    textLetter = None
    def wrapper(self, *args, **kwargs):
        sleep(0.5)
        lock1.acquire()
        nonlocal keyLetter, encoded, textLetter
        keyLetter = kwargs["keyLetter"] if "keyLetter" in kwargs else args[1]
        textLetter = kwargs["textLetter"] if "textLetter" in kwargs else args[0]
        encoded = function(self, *args, **kwargs)
        try:
            gui.drawNextEncodedLetter(keyLetter, textLetter, encoded)
        except:
            print("failed to visualize next encoded letter: ", keyLetter, textLetter, encoded)
            sys.exit(0)

        lock1.release()
        return encoded
    return wrapper

def string_encoder(function):
    global gui
    def wrapper(self, *args, **kwargs):
        res = function(self,*args,**kwargs)
        sleep(2)
        gui._clearFragment()
        return res
    return wrapper

def string_decoder(function):
    global gui
    def wrapper(self, *args, **kwargs):
        res = function(self,*args,**kwargs)
        sleep(2)
        gui._clearFragment()
        return res
    return wrapper

def letter_decode_decorator(function):
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



