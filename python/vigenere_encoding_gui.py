"""@package docstring
Documentation for this module.

More details.
"""

import threading
from time import sleep,time

import matplotlib
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
matplotlib.use('TkAgg')

from break_vigenere_encoding import CiphertextOnly,KnownPlainText,ChosenPlainText,ChosenCiphertext

try:
    import Tkinter as tk
except ImportError:
    import tkinter as tk

alphabet = [chr(x) for x in range(ord('a'), ord('z') + 1)]

"""Documentation for this class.

More details.
"""
class LaTeXFrame:
    dpi=40
    font_size = 30
    offset=5
    indent=5
    """Documentation for this function.

    More details.
    """
    def __init__(self, master:tk.Tk, pos, latex):
        self.fig = None
        self.ax = None
        self.master=master
        self.pos=pos
        self.latex=latex
        self.label = None
        self.mainframe = None
        self.canvas = None

    """Documentation for this function.

    More details.
    """
    def draw(self, size=(1,1), included=False):
        root = self.master

        self.mainframe = tk.Frame(root)

        self.mainframe.pack(side="left", anchor="s")
        self.label = tk.Frame(self.mainframe)
        if included:
            self.label.pack(side="top",anchor="w", fill="x",expand=True)
        else:
            self.label.pack(side="top",anchor="w")

        self.fig = matplotlib.figure.Figure(figsize=size, dpi=LaTeXFrame.dpi)
        self.ax = self.fig.add_subplot(111)

        self.canvas = FigureCanvasTkAgg(self.fig, master=self.label)

        self.canvas.get_tk_widget().pack(fill="x")

        self.canvas._tkcanvas.pack(fill="x")

        self.ax.get_xaxis().set_visible(False)
        self.ax.get_yaxis().set_visible(False)
        self.ax.spines['top'].set_visible(False)
        self.ax.spines['right'].set_visible(False)
        self.ax.spines['bottom'].set_visible(False)
        self.ax.spines['left'].set_visible(False)
        self.update()

    """Documentation for this function.

    More details.
    """
    def update(self):
        text = None
        if self.latex is None or len(self.latex.strip()) == 0:
            text = "$\\mathbb{}$"
        else:
            text = "$" + self.latex + "$"
        self.ax.clear()
        self.ax.text(0.2, 0.6, text, fontsize=LaTeXFrame.font_size)
        self.canvas.draw()

    """Documentation for this function.

    More details.
    """
    def remove(self):
        self.mainframe.destroy()

    """Documentation for this function.

    More details.
    """
    def drawNextTo(self, other,size=(1,1), included=False):
        self.pos=(other.pos[0] + LaTeXFrame.dpi + LaTeXFrame.offset, other.pos[1])
        self.draw(size, included)

"""Documentation for this class.

More details.
"""
class TestMethods:
    """Documentation for this function.

    More details.
    """
    @staticmethod
    def knownPlaintext(this):
        if this.lock.locked():
            return
        ciphertext = this.var1.get()
        plaintext = this.var2.get()
        try:
            key = KnownPlainText([plaintext],[ciphertext]).deduceKey().lower()
            this.key_var.set(key)
        except:
            this.key_var.set("<Error>")

    """Documentation for this function.

    More details.
    """
    @staticmethod
    def ciphertextOnly_deduceKeyWithUnsecureMessage(this):
        if this.lock.locked():
            return
        ciphertext = this.var1.get()
        prefix = this.var2.get()
        try:
            key = CiphertextOnly(ciphertext).deduceKeyWithUnsecureMessage(prefix).lower()
            this.key_var.set(key)
        except:
            this.key_var.set("<Error>")

    """Documentation for this function.

    More details.
    """
    @staticmethod
    def chosenPlaintext_deduceKey(this):
        if this.lock.locked():
            return
        def fun():
            ciphertext = this.var1.get()
            gui.enc.key=this.var2.get()
            try:
                key = ChosenPlainText(gui.enc,ciphertext).deduceKey().lower()
                this.key_var.set(key)
            except:
                this.key_var.set("<Error>")
            this.lock.release()
        t=threading.Thread(target=fun)
        t.start()
        this.lock.acquire()

    """Documentation for this function.

    More details.
    """
    @staticmethod
    def chosenCiphertext_deduceKey(this):
        if this.lock.locked():
            return
        def fun():
            ciphertext = this.var1.get()
            gui.enc.key=this.var2.get()
            try:
                key = ChosenCiphertext(gui.enc, ciphertext).deduceKey().lower()
                this.key_var.set(key)
                this.lock.release()
            except:
                this.key_var.set("<Error>")
        t = threading.Thread(target=fun)
        t.start()
        this.lock.acquire()

"""Documentation for this class.

More details.
"""
class TestMethodCanvas:
    """Documentation for this function.

    More details.
    """
    def __init__(self, master, test_method, lock, **kwargs):
        self.lock=lock
        self.master=master
        self.test_frame = tk.Frame(self.master, padx=20, pady=10)

        self.var1 = tk.StringVar(self.test_frame)
        self.var2 = tk.StringVar(self.test_frame)
        self.key_var = tk.StringVar(self.test_frame)


        def _encodingTest():
            test_method(self)

        self.label=None
        self.frames=[]
        if "label" in kwargs:
            self.label=tk.Label(self.test_frame,text=kwargs["label"], padx=2, pady=2,
                font="Arial 11 bold")
        self.var1_label=None
        self.var1_side="top"
        if "var1" in kwargs:
            self.frames.append(tk.Frame(self.test_frame))
            fr=self.frames[len(self.frames)-1]
            self.var1_entry = tk.Entry(fr, textvariable=self.var1)
            self.var1_label=tk.Label(fr,text=kwargs["var1"], padx=2, pady=2,
                font="Arial 10")
            self.var1_label.pack(side="left",anchor="w")
            self.var1_side="left"
        else:
            self.var1_entry = tk.Entry(self.test_frame, textvariable=self.var1)

        self.var2_label=None
        self.var2_side="top"
        if "var2" in kwargs:
            self.frames.append(tk.Frame(self.test_frame))
            fr=self.frames[len(self.frames)-1]
            self.var2_entry = tk.Entry(fr, textvariable=self.var2)
            self.var2_label=tk.Label(fr,text=kwargs["var2"], padx=2, pady=2,
                font="Arial 10")
            self.var2_label.pack(side="left",anchor="w")
            self.var2_side="left"
        else:
            self.var2_entry = tk.Entry(self.test_frame, textvariable=self.var2)

        self.output_entry = tk.Entry(self.test_frame, textvariable=self.key_var,
                                     fg="black", bg="white", bd=0, state="readonly",
                                     font="Comic_Sans 11 italic")

        self.btn_text=tk.StringVar(self.master)
        self.ciphertext_only_btn = tk.Button(self.test_frame, command=_encodingTest, textvariable=self.btn_text)

    """Documentation for this function.

    More details.
    """
    def draw(self, *args):
        if self.label is not None:
            self.label.pack(side="top",pady=10,anchor="w")
        if len(args)==0:
            args=["Deduce key"]
        self.btn_text.set(args[0])
        for x in self.frames:
            x.pack(side="top",anchor="w",fill="x",expand=True)
        self.var1_entry.pack(side=self.var1_side, padx=5, pady=5, fill="x", expand=True)
        self.var2_entry.pack(side=self.var2_side, padx=5, pady=5, fill="x", expand=True)
        self.output_entry.pack(side="top", padx=5, pady=5)
        self.ciphertext_only_btn.pack(side="top")
        self.test_frame.pack(side="left")


lock1=threading.Lock()
"""Documentation for this class.

More details.
"""
class VigenereEncodingGUI:
    letter_delay=0.05
    font= "16"
    clear_delay=0.01
    post_clear_delay=1.5
    max_frames=15
    w=1225
    h=500
    scr_size="%sx%s"%(w,h)

    """Documentation for this function.

    More details.
    """
    def __init__(self):
        self.enc=None
        self.operating_thread=None
        self.main=tk.Tk()
        self.main.geometry(VigenereEncodingGUI.scr_size)
        self.symbol_canvas = tk.Canvas(self.main,background="green")
        self.anim_interrupt_ev=threading.Event()

        self.animation_speed=tk.DoubleVar(self.main)
        self.animation_speed.set(10.0)

        self.controls_fr=tk.Frame(self.main)

        self.plaintext_var=tk.StringVar(self.controls_fr)
        self.plaintext_var.set("differential geometry")
        self.text_input=tk.Entry(self.controls_fr, textvariable=self.plaintext_var, font=VigenereEncodingGUI.font)

        self.key_var=tk.StringVar(self.controls_fr)
        self.key_var.set("curve")
        self.key_input=tk.Entry(self.controls_fr, textvariable=self.key_var, font=VigenereEncodingGUI.font)

        self.output_var=tk.StringVar(self.controls_fr)
        self.ciphertext_output=tk.Entry(self.controls_fr, textvariable=self.output_var,fg="black",bg="white",bd=0,state="readonly")

        self.btn_frame=tk.Frame(self.controls_fr)
        self.button_encode=tk.Button(self.btn_frame, command=self._encode_input, text="encode")
        self.button_decode=tk.Button(self.btn_frame, command=self._decode_input, text="decode")

        self.anim_fr = tk.Frame(self.controls_fr)

        self.anim_speed_entry=tk.Entry(self.anim_fr, textvariable=self.animation_speed)
        self.anim_interrupt_btn=tk.Button(self.anim_fr, command=self._interrupt, text="Interrupt")

        self.title=tk.Label(self.main,text="Vigenere encoding GUI: v1.0",
                            font="Comic_Sans 18", pady=15)
        self.title.pack(side="top")
        self.text_input.pack(side="top", padx=10, pady=10)
        self.key_input.pack(side="top", padx=10, pady=10)
        self.ciphertext_output.pack(side="top")
        self.button_encode.pack(side="left", padx=10, pady=10)
        self.button_decode.pack(side="left", padx=10, pady=10)
        self.btn_frame.pack(side="top")
        tk.Label(self.anim_fr,text="Animation speed", font="Arial 12").pack(side="top",anchor="w")
        self.anim_speed_entry.pack(side="left",anchor="w", padx=5, pady=5)
        self.anim_interrupt_btn.pack(side="left",anchor="w", padx=5, pady=5)
        self.controls_fr.pack(side="left", fill="y", pady=20)
        self.anim_fr.pack(side="top", pady=20, anchor="w", padx=20, fill="x")


        self.symbol_canvas.pack(side="top",anchor="w", fill="both", expand=True, padx=50,pady=10)
        self.tests_grid=tk.Frame(self.main)

        lock=threading.Lock()
        self.ciphertext_only = TestMethodCanvas(self.tests_grid,
            test_method=TestMethods.ciphertextOnly_deduceKeyWithUnsecureMessage,lock=lock,
            label="Method: Ciphertext only",var1="Ciphertext",var2="Prefix")
        self.known_plaintext = TestMethodCanvas(self.tests_grid,
            test_method=TestMethods.knownPlaintext,lock=lock,
            label="Method: Known plaintext",var1="Ciphertext",var2="Plaintext")
        self.chosen_plaintext = TestMethodCanvas(self.tests_grid,
            test_method=TestMethods.chosenPlaintext_deduceKey,lock=lock,
            label="Method: Chosen plaintext",var1="Plaintext",var2="Key")
        self.chosen_ciphertext = TestMethodCanvas(self.tests_grid,
            test_method=TestMethods.chosenCiphertext_deduceKey,lock=lock,
            label="Method: Known ciphertext",var1="Ciphertext",var2="Key")

        self.methods=[
            self.ciphertext_only,self.known_plaintext,
            self.chosen_plaintext,self.chosen_ciphertext
        ]
        self.method_args=[
            [],[],
            [],[]
        ]
        for i in range(len(self.methods)):
            self.methods[i].draw(*self.method_args[i])

        self.tests_grid.pack(side="left")

        self.frames=[
            tk.Frame(self.symbol_canvas, width=0, height=LaTeXFrame.dpi, background="white"),
            tk.Frame(self.symbol_canvas, width=0, height=LaTeXFrame.dpi, background="white"),
            tk.Frame(self.symbol_canvas, width=0, height=LaTeXFrame.dpi, background="white"),
            tk.Frame(self.symbol_canvas, width=0, height=LaTeXFrame.dpi, background="white"),
            tk.Frame(self.symbol_canvas, width=0, height=LaTeXFrame.dpi, background="white")
        ]
        self.letter_frames_count=3
        for x in self.frames:
            x.pack(side="top", fill="both", expand=True)
        self.last_symbol_encoded=[None]*len(self.frames)
        self.fragment_symbols=[]
        self.w=VigenereEncodingGUI.w
        self.h=VigenereEncodingGUI.h
        self.operator_str=" \\hspace{1} ( mod  \\hspace{0.5} 26 )"
        self.op1=self._drawNext("+"+self.operator_str, 1, _include=False, size=(VigenereEncodingGUI.max_frames,1))
        self.op2=self._drawNext("=", 3, _include=False, size=(VigenereEncodingGUI.max_frames,1))

    """Documentation for this function.

    More details.
    """
    def _interrupt(self):
        if self.operating_thread is None:
            return
        if self.anim_interrupt_ev.is_set():
            self.anim_interrupt_ev.clear()
            return
        self.anim_interrupt_ev.set()

    """Documentation for this function.

    More details.
    """
    def sleep(self, delay):
        t0=time()
        while not self.anim_interrupt_ev.is_set() and time()-t0<delay:
            pass
        if self.anim_interrupt_ev.is_set():
            raise Exception("interrupted")

    """Documentation for this function.

    More details.
    """
    def _encode_input(self):
        assert self.enc is not None
        if self.operating_thread is not None:
            return
        lock=threading.Lock()
        def _enc():
            nonlocal lock
            text = self.plaintext_var.get()
            key = self.key_var.get()
            self.enc.key = key
            self.op1.latex="+"+self.operator_str
            self.op1.update()
            if len(key)>0:
                try:
                    out=self.enc.encodeString(text)
                    self.output_var.set(out)
                except: pass
            self.operating_thread=None
            self.anim_interrupt_ev.clear()
            lock.release()
        self.operating_thread=threading.Thread(target=_enc, daemon=True)
        lock.acquire()
        self.operating_thread.start()

    """Documentation for this function.

    More details.
    """
    def _decode_input(self):
        assert self.enc is not None
        if self.operating_thread is not None:
            return
        lock = threading.Lock()
        def _dec():
            nonlocal lock
            text = self.plaintext_var.get()
            key = self.key_var.get()
            self.enc.key = key
            self.op1.latex="-"+self.operator_str
            self.op1.update()
            if len(key) > 0:
                try:
                    out=self.enc.decodeString(text).upper()
                    self.output_var.set(out)
                except: pass
            self.operating_thread = None
            self.anim_interrupt_ev.clear()
            lock.release()
        self.operating_thread = threading.Thread(target=_dec, daemon=True)
        lock.acquire()
        self.operating_thread.start()

    """Documentation for this function.

    More details.
    """
    def resize(self,w,h):
        scr_size="%sx%s"%(w,h)
        self.main.geometry(scr_size)
        self.w=w
        self.h=h

    """Documentation for this function.

    More details.
    """
    def drawNextLetter(self, keyLetter, textLetter, encoded, size=(1,1), include=True):
        self._drawNext(keyLetter, 2, size=size, _include=include)
        self._drawNext(textLetter, 0, size=size, _include=include)
        self._drawNext(encoded, 4, size=size, _include=include)

    """Documentation for this function.

    More details.
    """
    def _drawNext(self, latex, pos=0, offset=None, _include=True, size=(1,1)):
        w=offset
        if offset is None:
            w=LaTeXFrame.offset
        if self.last_symbol_encoded[pos] is None:
            sym=LaTeXFrame(self.frames[pos], (LaTeXFrame.offset, LaTeXFrame.offset + w * pos),latex)
            if _include:
                self.fragment_symbols.append(sym)
            sym.draw(size,_include)
            self.last_symbol_encoded[pos]=sym
        else:
            sym = LaTeXFrame(self.frames[pos], (0, 0),latex)
            if _include:
                self.fragment_symbols.append(sym)
            sym.drawNextTo(self.last_symbol_encoded[pos],size,_include)
            self.last_symbol_encoded[pos]=sym

        if len(self.fragment_symbols) > VigenereEncodingGUI.max_frames * self.letter_frames_count:
            for i in range(self.letter_frames_count):
                self.fragment_symbols[i].remove()
            self.fragment_symbols=self.fragment_symbols[self.letter_frames_count:]
        return sym

    """Documentation for this function.

    More details.
    """
    def _clearFragment(self,encoder=None):
        for x in self.fragment_symbols:
            x.remove()
            sleep(VigenereEncodingGUI.clear_delay)
        self.fragment_symbols=[]
        self.last_symbol_encoded=[None]*len(self.frames)

        if encoder is None:
            self.drawNextLetter("", "", "")

    def update(self):
        self.symbol_canvas.update()

    def mainloop(self):
        self.symbol_canvas.mainloop()

gui=None
lock2=threading.Lock()
"""Documentation for this function.

More details.
"""
def _initGui():
    global gui
    if gui is None:
        lock2.acquire()
        if gui is None:
            gui = VigenereEncodingGUI()
            gui._clearFragment()
        lock2.release()

"""Documentation for this function.

More details.
"""
main_initialized=False
def mainloop_handler(function):
    global gui,main_initialized
    if main_initialized:
        raise Exception("the program can have only one mainloop handler")
    main_initialized=True
    _initGui()
    def wrapper(*args, **kwargs):
        def func():
            gui._clearFragment(True)
            return function(*args,*kwargs)
        thr = threading.Thread(target=func, daemon=True)
        thr.start()
        gui.mainloop()
    return wrapper

"""Documentation for this function.

More details.
"""
def letter_encode_decorator(function):
    global gui,main_initialized
    if not main_initialized:
        _initGui()
    keyLetter = None
    encoded = None
    textLetter = None
    def wrapper(self, *args, **kwargs):
        if not main_initialized:
            return function(self, *args, **kwargs)
        gui.sleep(VigenereEncodingGUI.letter_delay/gui.animation_speed.get())
        lock1.acquire()
        nonlocal keyLetter, encoded, textLetter
        keyLetter = kwargs["keyLetter"] if "keyLetter" in kwargs else args[1]
        textLetter = kwargs["textLetter"] if "textLetter" in kwargs else args[0]
        encoded = "-"
        try:
            encoded = function(self, *args, **kwargs)
        except:
            pass
        gui.drawNextLetter(keyLetter, textLetter, encoded)
        lock1.release()
        return encoded
    return wrapper

"""Documentation for this function.

More details.
"""
def string_encoder(function):
    global gui,main_initialized
    if not main_initialized:
        _initGui()
    def wrapper(self, *args, **kwargs):
        if not main_initialized:
            return function(self, *args, **kwargs)
        gui._clearFragment(encoder=True)
        res = function(self,*args,**kwargs)
        sleep(VigenereEncodingGUI.post_clear_delay)
        gui._clearFragment(encoder=True)
        return res
    return wrapper

"""Documentation for this function.

More details.
"""
def string_decoder(function):
    global gui,main_initialized
    if not main_initialized:
        _initGui()
    def wrapper(self, *args, **kwargs):
        if not main_initialized:
            return function(self, *args, **kwargs)
        gui._clearFragment(encoder=False)
        res = function(self,*args,**kwargs)
        sleep(VigenereEncodingGUI.post_clear_delay)
        gui._clearFragment(encoder=False)
        return res
    return wrapper

"""Documentation for this function.

More details.
"""
def letter_decode_decorator(function):
    global gui,main_initialized
    if not main_initialized:
        _initGui()
    keyLetter = None
    decoded = None
    encodedLetter = None
    def wrapper(self, *args, **kwargs):
        if not main_initialized:
            return function(self, *args, **kwargs)
        gui.sleep(VigenereEncodingGUI.letter_delay/gui.animation_speed.get())
        nonlocal keyLetter, decoded, encodedLetter
        keyLetter = kwargs["keyLetter"] if "keyLetter" in kwargs else args[1]
        encodedLetter = kwargs["encodedLetter"] if "encodedLetter" in kwargs else args[0]
        decoded = "-"
        try:
            decoded = function(self, *args, **kwargs)
        except: pass
        gui.drawNextLetter(keyLetter, encodedLetter, decoded)
        return decoded
    return wrapper




