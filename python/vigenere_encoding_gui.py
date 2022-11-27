import sys
import threading
from time import sleep

import matplotlib
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
matplotlib.use('TkAgg')

try:
    import Tkinter as tk
except ImportError:
    import tkinter as tk

class LaTeXFrame:
    width=30
    height=30
    font_size = 14
    offset=5
    indent=5
    def __init__(self, master:tk.Tk, pos, latex):
        self.fig = None
        self.ax = None
        self.master=master
        self.pos=pos
        self.symbol=latex
        self.label = None
        self.mainframe = None
        self.canvas = None
    def draw(self):

        root = self.master

        self.mainframe = tk.Frame(root)
        self.mainframe.pack(side="left")

        self.label = tk.Label(self.mainframe)
        self.label.pack()

        self.fig = matplotlib.figure.Figure(figsize=(0.5, 0.5), dpi=100)
        self.ax = self.fig.add_subplot(111)

        self.canvas = FigureCanvasTkAgg(self.fig, master=self.label)
        self.canvas.get_tk_widget().pack()
        self.canvas._tkcanvas.pack()

        self.ax.get_xaxis().set_visible(False)
        self.ax.get_yaxis().set_visible(False)

        text = "abc"
        text = "$" + text + "$"
        self.ax.clear()
        self.ax.text(0.2, 0.6, text, fontsize=10)
        self.canvas.draw()

    def remove(self):
        self.mainframe.destroy()

    def drawNextTo(self, other):
        self.pos=(other.pos[0] + LaTeXFrame.width + LaTeXFrame.offset, other.pos[1])
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
        self.frames=[
            tk.Frame(self.screen, width=0, height=50, background="green"),
            tk.Frame(self.screen, width=0, height=50, background="red"),
            tk.Frame(self.screen, width=0, height=50, background="yellow")
        ]
        for x in self.frames:
            x.pack(side="top",fill="x", expand=True)
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
        s2=self._drawNextEncoded(keyLetter, 1)
        s1=self._drawNextEncoded(textLetter, 0)
        s3=self._drawNextEncoded(encoded, 2)

    def _drawNextEncoded(self,letter,pos=0,offset=None):
        w=offset
        if offset is None:
            w=LaTeXFrame.offset
        if self.last_symbol_encoded[pos] is None:
            sym=LaTeXFrame(self.frames[pos], (LaTeXFrame.offset, LaTeXFrame.offset + w * pos),
                           letter)
            self.fragment_symbols.append(sym)
            sym.draw()
            self.last_symbol_encoded[pos]=sym
            return sym
        else:
            sym = LaTeXFrame(self.frames[pos], (0, 0),
                             letter)
            self.fragment_symbols.append(sym)
            sym.drawNextTo(self.last_symbol_encoded[pos])
            self.last_symbol_encoded[pos]=sym
            return sym

    def _clearFragment(self):
        for x in self.fragment_symbols:
            x.remove()
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



