import re
import math

def calc_command_line():
    """Calculator with command line interface"""
    while True:
        my_string = input("Write the expression or exit (eg 2+2): ")
        my_string = my_string.replace(" ", "")
        if my_string == "exit":
            break
        if all(x in ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", ".", "+", "-", "*", "/", "(", ")", "√"] for x in my_string) is False:
            print("Incorrect symbols")
            continue
        try:
            test1 = re.sub(r"(\d)\(", r"\1*(", my_string)
            test2 = re.sub(r"(\d)√", r"\1*√", test1)
            test3 = re.sub(r"√(\d)", r"math.sqrt(\1)", test2)
            result = eval(test3)
            if str(result)[-2:] == ".0":
                print(int(result))
            else:
                print(result)
        except ZeroDivisionError:
            print("Can't divide by 0")
        except SyntaxError:
            print("Incorrect expression")

def calc_pysimplegui():
    """Calculator with PySimpleGUI interface"""
    import PySimpleGUI as sg
    # Window settings
    sg.theme("SystemDefault1")
    layout2 =[  [sg.Button("/"), sg.Button("⌫"), sg.Button("c")],
                [sg.Button("*"), sg.Button("^"), sg.Button("√")],
                [sg.Button("-"), sg.Button("("), sg.Button(")")],
                [sg.Button("+"), sg.Button("=")]]
    layout1 =[  [sg.Button("7"), sg.Button("8"), sg.Button("9")],
                [sg.Button("4"), sg.Button("5"), sg.Button("6")],
                [sg.Button("1"), sg.Button("2"), sg.Button("3")],
                [sg.Button("0"), sg.Button(".")]]
    layout = [  [sg.Input(size=(34,1), justification="right", key="-INPUT-", font=("Helvetica", 20))],
                [sg.Text(key="-OUTPUT-", justification="right", size=(45,1), font=("Helvetica", 15))],
                [sg.Column(layout1, pad=(0,0)), sg.Column(layout2, pad=(0,0))]]
    window = sg.Window("Calculator", layout, element_padding=2, element_justification="center", debugger_enabled=False, auto_size_buttons=False, default_button_element_size=(6,1), font=("Helvetica", 12, "bold"), return_keyboard_events=True, icon="data/calc.png")
    # Main loop
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED:
            break
        my_string = values["-INPUT-"]
        # Buttons events
        if event == "1":
            window["-INPUT-"].update(my_string + "1")
        if event == "2":
            window["-INPUT-"].update(my_string + "2")
        if event == "3":
            window["-INPUT-"].update(my_string + "3")
        if event == "4":
            window["-INPUT-"].update(my_string + "4")
        if event == "5":
            window["-INPUT-"].update(my_string + "5")
        if event == "6":
            window["-INPUT-"].update(my_string + "6")
        if event == "7":
            window["-INPUT-"].update(my_string + "7")
        if event == "8":
            window["-INPUT-"].update(my_string + "8")
        if event == "9":
            window["-INPUT-"].update(my_string + "9")
        if event == "0":
            window["-INPUT-"].update(my_string + "0")
        if event == ".":
            window["-INPUT-"].update(my_string + ".")
        if event == "+":
            window["-INPUT-"].update(my_string + "+")
        if event == "-":
            window["-INPUT-"].update(my_string + "-")
        if event == "*":
            window["-INPUT-"].update(my_string + "*")
        if event == "/":
            window["-INPUT-"].update(my_string + "/")
        if event == "(":
            window["-INPUT-"].update(my_string + "(")
        if event == ")":
            window["-INPUT-"].update(my_string + ")")
        if event == "^":
            window["-INPUT-"].update(my_string + "^")
        if event == "√":
            window["-INPUT-"].update(my_string + "√")
        if event == "⌫":
            window["-INPUT-"].update(my_string[:-1])
        if event == "c":
            window["-INPUT-"].update(my_string.replace(my_string, ""))
            window["-OUTPUT-"].update("")
        # Tests and operations
        try:
            if event == "=" or event == "KP_Enter:104" or event == "Return:36":
                if all(x in ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", ".", "+", "-", "*", "/", "(", ")", "√", "^"] for x in my_string) is False:
                    window["-OUTPUT-"].update("Incorrect symbols")
                    continue
                test0 = re.sub(r"\^", r"**", my_string)
                test1 = re.sub(r"(\d)\(", r"\1*(", test0)
                test2 = re.sub(r"(\d)√", r"\1*√", test1)
                test3 = re.sub(r"√(\d)", r"math.sqrt(\1)", test2)
                result = eval(test3)
                if str(result)[-2:] == ".0":
                    window["-INPUT-"].update(int(result))
                else:
                    window["-INPUT-"].update(result)
                window["-OUTPUT-"].update(my_string)
        except ZeroDivisionError:
            window["-OUTPUT-"].update("Can't divide by 0")
        except SyntaxError:
            window["-OUTPUT-"].update("Incorrect expression")

def calc_tkinter():
    """Calculator with Tkinter interface"""
    import tkinter as tk
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
    # Window settings
    window = tk.Tk(className="calc")
    window.resizable(False, False)
    window.title("Calculator")
    window.iconphoto(False, tk.PhotoImage(file='data/calc.png'))
    frame = tk.Frame(window, border=5)
    frame.pack()
    entry = tk.Entry(frame, width=35, font="size= 16", justify="right", highlightcolor="white", highlightthickness=0)
    entry.grid(column=0, row=1, columnspan=6)
    entry.focus_set()
    label = tk.Label(frame, width=40, font="size= 14", anchor="e")
    label.grid(column=0, row=2, columnspan=6)
    # Buttons
    def my_button(text_b, col, row):
        tk.Button(frame, text=text_b, height=1, width=6, font=("Helvetica", 12, "bold"), command=lambda: insert(text_b), relief="groove").grid(column=col, row=row)
    def my_button1(text_b, op, col, row):
        tk.Button(frame, text=text_b, height=1, width=6, font=("Helvetica", 12, "bold"), command=op, relief="groove").grid(column=col, row=row)
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

if __name__ == "__main__":
    # calc_tkinter()
    # calc_pysimplegui()
    # calc_command_line()
    calc_tkinter()