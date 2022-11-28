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
    dpi=40
    font_size = 30
    offset=5
    indent=5
    def __init__(self, master:tk.Tk, pos, latex):
        self.fig = None
        self.ax = None
        self.master=master
        self.pos=pos
        self.latex=latex
        self.label = None
        self.mainframe = None
        self.canvas = None
    def draw(self, size=(1,1)):
        root = self.master

        self.mainframe = tk.Frame(root)
        self.mainframe.pack(side="left")

        self.label = tk.Frame(self.mainframe)
        self.label.pack(fill="both")

        self.fig = matplotlib.figure.Figure(figsize=size, dpi=LaTeXFrame.dpi)
        self.ax = self.fig.add_subplot(111)

        self.canvas = FigureCanvasTkAgg(self.fig, master=self.label)
        self.canvas.get_tk_widget().pack(fill="both")
        self.canvas._tkcanvas.pack(fill="both")

        self.ax.get_xaxis().set_visible(False)
        self.ax.get_yaxis().set_visible(False)
        self.ax.spines['top'].set_visible(False)
        self.ax.spines['right'].set_visible(False)
        self.ax.spines['bottom'].set_visible(False)
        self.ax.spines['left'].set_visible(False)
        text=None
        if self.latex is None or len(self.latex)==0:
            text="$\\mathbb{}$"
        else:
            text = "$" + self.latex + "$"
        self.ax.clear()
        self.ax.text(0.2, 0.6, text, fontsize=LaTeXFrame.font_size)
        self.canvas.draw()

    def remove(self):
        self.mainframe.destroy()

    def drawNextTo(self, other,size=(1,1)):
        self.pos=(other.pos[0] + LaTeXFrame.dpi + LaTeXFrame.offset, other.pos[1])
        self.draw(size)

lock1=threading.Lock()
class VigenereEncodingGUI:
    letter_delay=0.3
    clear_delay=0.05
    max_frames=7
    w=500
    h=LaTeXFrame.dpi*4
    scr_size="%sx%s"%(w,h)
    def __init__(self):
        self.main=tk.Tk()
        self.main.geometry(VigenereEncodingGUI.scr_size)
        self.screen = tk.Canvas(self.main)
        self.screen.pack(expand=True)
        self.text_input=None
        self.ciphertext_output=None
        self.button_encode=None
        self.button_decode=None
        self.frames=[
            tk.Frame(self.screen, width=0, height=LaTeXFrame.dpi),
            tk.Frame(self.screen, width=0, height=LaTeXFrame.dpi),
            tk.Frame(self.screen, width=0, height=LaTeXFrame.dpi),
            tk.Frame(self.screen, width=0, height=LaTeXFrame.dpi),
            tk.Frame(self.screen, width=0, height=LaTeXFrame.dpi)
        ]
        self.letter_frames_count=3
        for x in self.frames:
            x.pack(side="top",fill="both", expand=True)
        self.last_symbol_encoded=[None]*len(self.frames)
        self.fragment_symbols=[]
        self.w=VigenereEncodingGUI.w
        self.h=VigenereEncodingGUI.h
        self._drawNext("+ (mod 26)", 1, _include=False, size=(VigenereEncodingGUI.max_frames,1))
        self._drawNext("=", 3, _include=False, size=(VigenereEncodingGUI.max_frames,1))

    def resize(self,w,h):
        scr_size="%sx%s"%(w,h)
        self.main.geometry(scr_size)
        self.w=w
        self.h=h

    def drawNextLetter(self, keyLetter, textLetter, encoded):
        self._drawNext(keyLetter, 2)
        self._drawNext(textLetter, 0)
        self._drawNext(encoded, 4)

    def _drawNext(self, latex, pos=0, offset=None, _include=True, size=(1,1)):
        w=offset
        if offset is None:
            w=LaTeXFrame.offset
        if self.last_symbol_encoded[pos] is None:
            sym=LaTeXFrame(self.frames[pos], (LaTeXFrame.offset, LaTeXFrame.offset + w * pos),latex)
            if _include:
                self.fragment_symbols.append(sym)
            sym.draw(size)
            self.last_symbol_encoded[pos]=sym
        else:
            sym = LaTeXFrame(self.frames[pos], (0, 0),latex)
            if _include:
                self.fragment_symbols.append(sym)
            sym.drawNextTo(self.last_symbol_encoded[pos],size)
            self.last_symbol_encoded[pos]=sym

        if len(self.fragment_symbols) > VigenereEncodingGUI.max_frames * self.letter_frames_count:
            for i in range(self.letter_frames_count):
                self.fragment_symbols[i].remove()
            self.fragment_symbols=self.fragment_symbols[self.letter_frames_count:]
        return sym

    def _clearFragment(self):
        for x in self.fragment_symbols:
            x.remove()
            sleep(VigenereEncodingGUI.clear_delay)
        self.fragment_symbols=[]
        self.last_symbol_encoded=[None]*len(self.frames)
        self.drawNextLetter("","","")

    def drawNextDecodedLetter(self,keyLetter, encodedLetter, decoded):
        pass
    def update(self):
        self.screen.update()

    def mainloop(self):
        self.screen.mainloop()

class BreakVigenereEncodingGUI:
    def __init__(self, screen):
        self.screen = screen



def mainloop_handler(function):
    global gui
    gui = VigenereEncodingGUI()
    gui._clearFragment()
    def wrapper(*args, **kwargs):
        def func():
            return function(*args,*kwargs)
        thr = threading.Thread(target=func, daemon=True)
        thr.start()
        gui.mainloop()
    return wrapper


def letter_encode_decorator(function):
    global gui
    keyLetter = None
    encoded = None
    textLetter = None
    def wrapper(self, *args, **kwargs):
        sleep(VigenereEncodingGUI.letter_delay)
        lock1.acquire()
        nonlocal keyLetter, encoded, textLetter
        keyLetter = kwargs["keyLetter"] if "keyLetter" in kwargs else args[1]
        textLetter = kwargs["textLetter"] if "textLetter" in kwargs else args[0]
        encoded = function(self, *args, **kwargs)
        gui.drawNextLetter(keyLetter, textLetter, encoded)
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
        sleep(VigenereEncodingGUI.letter_delay)
        nonlocal keyLetter, decoded, encodedLetter
        keyLetter = kwargs["keyLetter"] if "keyLetter" in kwargs else args[1]
        encodedLetter = kwargs["encodedLetter"] if "encodedLetter" in kwargs else args[0]
        decoded = function(self, *args, **kwargs)
        gui.drawNextLetter(keyLetter, encodedLetter, decoded)
        return decoded
    return wrapper



