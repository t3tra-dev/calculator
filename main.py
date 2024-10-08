import sys
import tkinter as tk
from tkinter import ttk

import sympy
import matplotlib
import matplotlib.pyplot as plt
from sympy.parsing.latex import parse_latex
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

matplotlib.use('TkAgg')

root = tk.Tk()
root.title('Calculator')
root.geometry('585x170+100+100')
root.resizable(0, 0)
root.attributes("-topmost", True)

fig = None
canvas = None


def copy():
    root.clipboard_append(result_label['text'])


def expand():
    raw = entry_var.get()
    val = parse_latex(raw)
    try:
        r = sympy.expand(val)
    except Exception as e:
        r = str(e)
    finally:
        result_label['text'] = sympy.latex(r)
        update_latex_display(expr_in=raw, expr_out=r)

def factor():
    raw = entry_var.get()
    val = parse_latex(raw)
    try:
        r = sympy.factor(val)
    except Exception as e:
        r = str(e)
    finally:
        result_label['text'] = sympy.latex(r)
        update_latex_display(expr_in=raw, expr_out=r)


def update_latex_display(expr_in, expr_out):
    global fig, canvas
    if fig is not None:
        fig.clear()
        canvas.get_tk_widget().destroy()
    fig = plt.figure(figsize=(5.6, 0.6), dpi=100)
    ax = fig.add_subplot(111)
    ax.text(0.5, 0.5, rf'$ {expr_in} = {sympy.latex(expr_out)} $', ha='center', va='center', size=14)
    ax.set_axis_off()
    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.draw()
    canvas.get_tk_widget().place(x=10, y=94)


def on_closing():
    global fig
    if fig is not None:
        plt.close(fig)
    root.destroy()
    sys.exit()


entry_var = tk.StringVar()
entry = ttk.Entry(width=35, textvariable=entry_var)
btn_exp = ttk.Button(text='展開', width=6, command=expand)
btn_fac = ttk.Button(text='因数分解', width=6, command=factor)
result_label = tk.Label(text='result', width=48, background='#222')
btn_copy = ttk.Button(text='copy', width=6, command=copy)

entry.place(x=16, y=12)
btn_exp.place(x=360, y=12)
btn_fac.place(x=470, y=12)
result_label.place(x=18, y=52)
btn_copy.place(x=470, y=49)

root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()
