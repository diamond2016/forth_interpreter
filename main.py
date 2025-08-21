from tkinter import *
from tkinter import messagebox
import json
import os


BACKGROUND_COLOR = "#B1DDC6"
DEFAULT_CMDS = ["+", "-", "*", "/", "mod",
                "dup", "drop", "swap", "over", "rot", ".", "emit", "cr", ".\"","bye"]

# ---------------------------- FUNCTION: LOAD/WRITE STACK STATE ----------------#
# json file {"words:" [{"id:": 9, "value": "val"}, ...]}


def load_forth_dict():
    global word_stack
    if os.path.exists("forth_dict.json"):
        with open("forth_dict.json", "r") as file:
            d = json.load(file)
            my_list = d["words"]
            word_stack = [my_list[i]["value"] for i in range(len(my_list))]


def save_forth_dict():
    global word_stack
    with open("forth_dict.json", "w") as file:
        forth_dict = {"words": []}
        for i in range(len(word_stack)):
            word = {"id": i, "value": word_stack[i]}
            forth_dict["words"].append(word)
        json.dump(forth_dict, file)

 # ---------------------------- FUNCTION: LOAD/WRITE FORTH CMD ----------------#
# json file {"cmds:" [{"id:": 0, "value": "+"}, ...]}


def load_forth_cmd_dict():
    global word_cmd
    if os.path.exists("forth_cmd.json"):
        with open("forth_cmd_dict.json", "r") as file:
            d = json.load(file)
            my_list = d["cmds"]
            word_cmd = [my_list[i]["value"] for i in range(len(my_list))]
            for cmd in DEFAULT_CMDS:
                if cmd not in word_cmd:
                    word_cmd.append(cmd)
            word_cmd.sort()  # Sort the commands alphabetically
    else:
        # Initialize with default commands if file does not exist
        word_cmd = DEFAULT_CMDS.copy()


def save_forth_cmd_dict():
    global word_cmd
    with open("forth_cmd_dict.json", "w") as file:
        forth_cmd_dict = {"cmds": []}
        for i in range(len(word_cmd)):
            word = {"id": i, "value": word_cmd[i]}
            forth_cmd_dict["cmds"].append(word)
        json.dump(forth_cmd_dict, file)

# ---------------------------- FUNCTION: PEEK_NUMBER -----------------------#


def peek_number():
    l = len(word_stack)
    if l == 0:
        return -1
    try:
        int_val = int(word_stack[l - 1])
    except ValueError:
        return -1
    else:
        return int_val
# ---------------------------- FUNCTION: POP_NUMBER ------------------------#


def pop_number():
    int_val = peek_number()
    if int_val != -1:
        word_stack.pop()
    return int_val
# ---------------------------- FUNCTION: EVAL -----------------------#


def op_eval(op1, op2, command):
    if command == "+":
        return op1 + op2
    elif command == "-":
        return op1 - op2
    elif command == "*":
        return op1 * op2
    elif command == "/":
        if op2 == 0:
            messagebox.showerror("Error", "Division by zero is not allowed.")
            return -1
        return op1 // op2  # Integer division
    elif command == "mod":
        if op2 == 0:
            messagebox.showerror("Error", "Division by zero is not allowed.")
            return -1
        return op1 % op2
    else:
        messagebox.showerror("Error", "Unknown operation.")
        return -1
# ---------------------------- FUNCTION: MANAGE_COMMANDS -----------------------#


def manage_commands(command, next_command):
    global word_stack
    global data_message_text

    if command == "+" or command == "-" or command == "*" or command == "/" or command == "mod":
        op1 = pop_number()
        op2 = pop_number()
        if op1 != -1 and op2 != -1:
            result = op_eval(op1, op2, command)
            word_stack.append(result)
            return 0
        else:
            return -1
    elif command == "dup": 
        if peek_number() != -1:
            word_stack.append(word_stack[-1])
            return 0
        else:
            messagebox.showerror("Error", "Stack is empty, cannot duplicate.")
    elif command == "drop":
        if peek_number() != -1:
            word_stack.pop()
            return 0
        else:
            messagebox.showerror("Error", "Stack is empty, cannot drop.") 
    elif command == "swap":
        if len(word_stack) < 2:
            messagebox.showerror("Error", "Not enough elements to swap.")
        else:
            word_stack[-1], word_stack[-2] = word_stack[-2], word_stack[-1]
            return 0
    elif command == "over":
        if len(word_stack) < 2:
            messagebox.showerror("Error", "Not enough elements to over.")
        else:
            word_stack.append(word_stack[-2])
            return 0
    elif command == "rot":
        if len(word_stack) < 3:
            messagebox.showerror("Error", "Not enough elements to rotate.")
        else:
            word_stack.append(word_stack.pop(-3))
            return 0
    elif command == ".":
        if peek_number() != -1:
            data_message_text = data_message_text + str(word_stack.pop())
            write_message()
            return 0
    elif command == "emit":
        if peek_number() != -1:
            ch = pop_number()
            data_message_text = data_message_text + chr(ch)
            write_message()
            return 0
    elif command == "cr":
        if peek_number() != -1:
            data_message_text = data_message_text + "'\n'"
            write_message()
            return 0
    elif command == ".\"":
        print(next_command)
        data_message_text = data_message_text + next_command[0:-1]
        write_message()
        return 0
    elif command == "bye":
        save_dicts()
        window.quit()
# ---------------------------- FUNCTION: ENTER -----------------------#


def enter():
    global word_stack

    words = input_text.get().strip().split()
    i = 0
    for i in range (len(words)):
        word = words[i]
        next_word = ""
        if i+1 < len(words):
            next_word = words[i+1]

        if word in word_cmd:
            result = manage_commands(word, next_word)
            if result == -1:
                return
        else:
            if type(word) is int:
                word_stack.append(int(word))
        write_stack()
    input_text.delete(0, END)
# ---------------------------- FUNCTION: WRITE_MESSAGE-----------------#


def write_message():
    global data_message_text
    global data_message_var
    data_message_var.set(data_message_text)

# ---------------------------- FUNCTION: WRITE_STACK -----------------#


def write_stack():
    global data_stack_text
    data_stack_text = str(word_stack)
    data_stack_var.set(data_stack_text)

# ---------------------------- FUNCTION: SAVE_DICTS -----------------#


def save_dicts():
    save_forth_dict()
    save_forth_cmd_dict()
    messagebox.showinfo("Save", "Forth state saved successfully.")
# ---------------------------- FUNCTION: WRITE_PROMPT -----------------#


def write_prompt():
    global data_prompt_text
    data_prompt_var.set(data_prompt_text)


# ---------------------------- UI SETUP ------------------------------- #
word_stack = []
load_forth_dict()  # Load the initial stack from the JSON file
word_cmd = []
load_forth_cmd_dict()  # Load the initial commands from the JSON file

# --------------------------- MAIN -------------------------------------#
window = Tk()
window.title("Forth Interpreter")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

# label var
data_stack_text = str(word_stack)
data_message_text = ""
data_prompt_text = "ok>"
data_stack_var = StringVar()
data_message_var = StringVar()
data_prompt_var = StringVar()
data_stack_var.set(data_stack_text)
data_message_var.set(data_message_text)
data_prompt_var.set(data_prompt_text)

# canvas
canvas = Canvas(window, height=300, width=400,
                bg=BACKGROUND_COLOR, highlightthickness=0)
canvas.grid(row=0, column=0, columnspan=2, padx=20, pady=20)

# Text in canvas
stack_label = Label(canvas, text="stack", fg="black", bg=BACKGROUND_COLOR)
stack_label.grid(row=0, column=0)
input_label = Label(canvas, text="input", fg="black", bg=BACKGROUND_COLOR)
input_label.grid(row=1, column=0)
message_label = Label(canvas, text="message", fg="black", bg=BACKGROUND_COLOR)
message_label.grid(row=2, column=0, rowspan=2)


stack_text = Label(canvas, font=("Ariel", 14),
                   textvariable=data_stack_var, fg="black", bg=BACKGROUND_COLOR)
stack_text.grid(row=0, column=1, columnspan=2)
prompt_text = Label(canvas, font=("Ariel", 16, "bold"),
                    textvariable=data_prompt_var, fg="black", bg=BACKGROUND_COLOR)
prompt_text.grid(row=1, column=1)
input_text = Entry(canvas, font=("Ariel", 16, "italic"),
                   fg="black", bg=BACKGROUND_COLOR)
input_text.grid(row=1, column=2)
message_text = Label(canvas, font=(
    "Ariel", 14), textvariable=data_message_var, fg="black", bg=BACKGROUND_COLOR)
message_text.grid(row=2, column=1)

# Buttons
button_command = Button(canvas, text="<Enter word>",
                        highlightthickness=0, command=enter)
button_command.grid(row=4, column=1)
button_command = Button(canvas, text="<Save state>",
                        highlightthickness=0, command=save_dicts)
button_command.grid(row=4, column=2)

window.mainloop()
