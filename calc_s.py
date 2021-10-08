import re
import math

while True:
    my_string = input("Write the equation or exit: ")
    if my_string == "exit":
        break
    if all(x in ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", ".", "+", "-", "*", "/", "(", ")", "√"] for x in my_string) is False:
        print("Incorrect symbols")
        continue
    try:  
        test1 = re.sub(r"(\d)\(", r"\1*(", my_string)
        test2 = re.sub(r"(\d)√", r"\1*√", test1)
        test3 = re.sub(r"√(\d)", r"math.sqrt(\1)", test2)

        print(my_string)
        print(test3)

        result = eval(test3)
        if str(result)[-2:] == ".0":
            print(int(result))
        else:
            print(result)

    except ZeroDivisionError:
        print("Can't divide by 0")
    except SyntaxError:
        print("Incorrect equation")