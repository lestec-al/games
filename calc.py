import PySimpleGUI as sg
import re
import math

# App theme & icon
sg.theme("SystemDefault1")
icon = r"/images/icon.png"

# The buttons inside window
layout3 =[  [sg.Button("=", size=(15,1))]]
layout2 =[  [sg.Button("/"), sg.Button("⌫"), sg.Button("c")],
            [sg.Button("*"), sg.Button("^"), sg.Button("√")],
            [sg.Button("-"), sg.Button("("), sg.Button(")")],
            [sg.Button("+"), sg.Column(layout3, justification="center")]]
layout1 =[  [sg.Button("7"), sg.Button("8"), sg.Button("9")],
            [sg.Button("4"), sg.Button("5"), sg.Button("6")],
            [sg.Button("1"), sg.Button("2"), sg.Button("3")],
            [sg.Button("0"), sg.Button(".")]]
layout = [  [sg.Input(size=(34,1), justification="right", key="-INPUT-", font=("Helvetica", 20))],
            [sg.Text(key="-OUTPUT-", justification="right", size=(45,1), font=("Helvetica", 15))],
            [sg.Column(layout1, pad=(0,0)), sg.Column(layout2, pad=(0,0))]]

# The Window itself param
window = sg.Window("Simple Calculator", layout, element_padding=2, element_justification="center", debugger_enabled=False, auto_size_buttons=False, default_button_element_size=(6,1), font=("Helvetica", 12, "bold"), return_keyboard_events=True, icon=icon)

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

    # Operation
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
        window["-OUTPUT-"].update("Incorrect equation")