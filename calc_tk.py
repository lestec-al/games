import tkinter as tk
import re
import math
# Operations
def insert(char):
    entry.insert("end", char)
def delete():
    entry.delete(0, "end")
    label["text"]=""
def delete1():
    entry.delete(entry.index("end") - 1)
def operation():
    my_string = entry.get()
    try:
        if all(x in ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", ".", "+", "-", "*", "/", "(", ")", "√", "^"] for x in my_string) is False:
            label["text"]="Incorrect symbols"
            return None
        test0 = re.sub(r"\^", r"**", my_string)
        test1 = re.sub(r"(\d)\(", r"\1*(", test0)
        test2 = re.sub(r"(\d)√", r"\1*√", test1)
        test3 = re.sub(r"√(\d)", r"math.sqrt(\1)", test2)
        result = eval(test3)
        entry.delete(0, "end")
        if str(result)[-2:] == ".0":
            entry.insert("end", int(result))
        else:
            entry.insert("end", result)
        label["text"]=my_string
    except ZeroDivisionError:
        label["text"]="Can't divide by 0"
    except SyntaxError:
        label["text"]="Incorrect expression"
# Window
window = tk.Tk(className="calc")
window.resizable(False, False)
window.title("Simple Calculator")
window.iconphoto(False, tk.PhotoImage(file='images/calc.png'))
# The staff inside window
entry = tk.Entry(window, width=35, font="size= 16", justify="right", highlightcolor="white", highlightthickness=0)
entry.grid(column=0, row=1, columnspan=6)
entry.focus_set()
label = tk.Label(window, width=40, font="size= 14", anchor="e")
label.grid(column=0, row=2, columnspan=6)
# Buttons models
def my_button(text_b, col, row):
    button = tk.Button(window, text=text_b, height=1, width=6, font=("Helvetica", 12, "bold"), command=lambda: insert(text_b)).grid(column=col, row=row)
def my_button1(text_b, op, col, row):
    button = tk.Button(window, text=text_b, height=1, width=6, font=("Helvetica", 12, "bold"), command=op).grid(column=col, row=row)
# Buttons
my_button("7", 0, 3), my_button("8", 1, 3), my_button("9", 2, 3)
my_button("4", 0, 4), my_button("5", 1, 4), my_button("6", 2, 4)
my_button("1", 0, 5), my_button("2", 1, 5), my_button("3", 2, 5)
my_button("0", 0, 6), my_button(".", 1, 6)
my_button("/", 3, 3), my_button1("⌫", delete1, 4, 3), my_button1("c", delete, 5, 3)
my_button("*", 3, 4), my_button("^", 4, 4), my_button("√", 5, 4)
my_button("-", 3, 5), my_button("(", 4, 5), my_button(")", 5, 5)
my_button("+", 3, 6), my_button1("=", operation, 4, 6)
# Keyboard
window.bind("<Return>", lambda event:operation())
window.bind("<KP_Enter>", lambda event:operation())
window.mainloop()