import os
import subprocess

from enum import Enum
from tkinter import *
from tkinter import ttk

root = Tk()
root.title("Standard Calculator")


def donothing():
    pass


menubar = Menu(root)
filemenu = Menu(menubar, tearoff=0)
filemenu.add_command(label="Scientific Calculator", command=donothing)
filemenu.add_command(label="Exit Application", command=exit)
menubar.add_cascade(label="File", menu=filemenu)

helpmenu = Menu(menubar, tearoff=0)
helpmenu.add_command(label="About Application", command=donothing)
menubar.add_cascade(label="Help", menu=helpmenu)


class ArithmeticOperation(Enum):
    ADDITION = 1
    SUBTRACTION = 2
    MULTIPLICATION = 3
    DIVISION = 4


class FixedWidthButton(ttk.Button):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, width=4)


class NumberButton(FixedWidthButton):
    pass


class ArithmeticOperationButton(FixedWidthButton):
    pass


class SpecialOperationButton(FixedWidthButton):
    pass


shadow_operands = ""
current_number = ""  # Track current number being inputted so that we could validate it
operands = StringVar()
digits = StringVar()

memory = 0


def mplus():
    global memory
    global shadow_operands

    value_now = eval(shadow_operands)
    memory += value_now
    operands.set(f"M+ {value_now}")
    digits.set(str(memory))


def mminus():
    global memory
    global shadow_operands

    value_now = eval(shadow_operands)
    memory -= value_now
    operands.set(f"M- {value_now}")
    digits.set(str(memory))


def mclear():
    global digits
    global current_number
    global memory
    global operands
    global shadow_operands

    memory = 0
    shadow_operands = ""
    current_number = ""
    operands.set("")
    digits.set("")


def mrecall():
    global memory
    global shadow_operands

    operands.set("")
    digits.set(str(memory))


def append_to_digit(new_digit: str):
    global current_number
    global digits
    global shadow_operands

    if new_digit == "." and "." in current_number:
        return

    current_number += new_digit
    shadow_operands += new_digit

    _digits = digits.get()
    digits.set(_digits + new_digit)


def clear_buffers():
    global current_number
    global digits
    global operands
    global shadow_operands

    current_number = ""
    shadow_operands = ""
    digits.set("")
    operands.set("")


def clear_last_number():
    global current_number
    global digits
    global shadow_operands

    current_number = current_number[:-1]
    shadow_operands = shadow_operands[:-1]
    digits.set(digits.get()[:-1])


def try_arithmetic(operation: ArithmeticOperation):
    global current_number
    global digits
    global shadow_operands

    operations = {
        ArithmeticOperation.ADDITION: ("+", "+"),
        ArithmeticOperation.SUBTRACTION: ("-", "-"),
        ArithmeticOperation.MULTIPLICATION: ("*", "×"),
        ArithmeticOperation.DIVISION: ("/", "÷"),
    }

    if current_number:
        digits.set(digits.get() + operations[operation][1])
        shadow_operands += operations[operation][0]

    current_number = ""


def compute():
    global digits
    global operands
    global shadow_operands

    operands.set(digits.get())
    digits.set(eval(shadow_operands))


def negate():
    pass


mainframe = ttk.Frame(root, padding="3 3 12 12")
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

ttk.Label(mainframe, textvariable=operands).grid(
    column=0, row=0, columnspan=4, sticky=(W,)
)
ttk.Label(mainframe, textvariable=digits).grid(
    column=0, row=1, columnspan=4, rowspan=2, sticky=(W,)
)

SpecialOperationButton(mainframe, text="C", command=clear_last_number).grid(
    column=0, row=3, sticky=(W,)
)
SpecialOperationButton(mainframe, text="AC", command=clear_buffers).grid(
    column=1, row=3, sticky=(W,)
)
SpecialOperationButton(mainframe, text="+/-", command=negate).grid(
    column=2, row=3, sticky=(W,)
)
ArithmeticOperationButton(
    mainframe, text="÷", command=lambda: try_arithmetic(ArithmeticOperation.DIVISION)
).grid(column=3, row=3, sticky=(W,))

NumberButton(mainframe, text="7", command=lambda: append_to_digit("7")).grid(
    column=0, row=4, sticky=(W,)
)
NumberButton(mainframe, text="8", command=lambda: append_to_digit("8")).grid(
    column=1, row=4, sticky=(W,)
)
NumberButton(mainframe, text="9", command=lambda: append_to_digit("9")).grid(
    column=2, row=4, sticky=(W,)
)
ArithmeticOperationButton(
    mainframe,
    text="×",
    command=lambda: try_arithmetic(ArithmeticOperation.MULTIPLICATION),
).grid(column=3, row=4, sticky=(W,))
SpecialOperationButton(mainframe, text="M+", command=mplus).grid(
    column=4, row=4, sticky=(W,)
)

NumberButton(mainframe, text="4", command=lambda: append_to_digit("4")).grid(
    column=0, row=5, sticky=(W,)
)
NumberButton(mainframe, text="5", command=lambda: append_to_digit("5")).grid(
    column=1, row=5, sticky=(W,)
)
NumberButton(mainframe, text="6", command=lambda: append_to_digit("6")).grid(
    column=2, row=5, sticky=(W,)
)
ArithmeticOperationButton(
    mainframe, text="-", command=lambda: try_arithmetic(ArithmeticOperation.SUBTRACTION)
).grid(column=3, row=5, sticky=(W,))
SpecialOperationButton(mainframe, text="M-", command=mminus).grid(
    column=4, row=5, sticky=(W,)
)

NumberButton(mainframe, text="1", command=lambda: append_to_digit("1")).grid(
    column=0, row=6, sticky=(W,)
)
NumberButton(mainframe, text="2", command=lambda: append_to_digit("2")).grid(
    column=1, row=6, sticky=(W,)
)
NumberButton(mainframe, text="3", command=lambda: append_to_digit("3")).grid(
    column=2, row=6, sticky=(W,)
)
ArithmeticOperationButton(
    mainframe, text="+", command=lambda: try_arithmetic(ArithmeticOperation.ADDITION)
).grid(column=3, row=6, sticky=(W,))
SpecialOperationButton(mainframe, text="MC", command=mclear).grid(
    column=4, row=6, sticky=(W,)
)

NumberButton(mainframe, text="00", command=lambda: append_to_digit("00")).grid(
    column=0, row=7, sticky=(W,)
)
NumberButton(mainframe, text="0", command=lambda: append_to_digit("0")).grid(
    column=1, row=7, sticky=(W,)
)
NumberButton(mainframe, text=".", command=lambda: append_to_digit(".")).grid(
    column=2, row=7, sticky=(W,)
)
ArithmeticOperationButton(mainframe, text="=", command=compute).grid(
    column=3, row=7, sticky=(W,)
)
SpecialOperationButton(mainframe, text="MR", command=mrecall).grid(
    column=4, row=7, sticky=(W,)
)

root.config(menu=menubar)
root.mainloop()
