from tkinter import *
from tkinter import messagebox
import json
import os


BACKGROUND_COLOR = "#B1DDC6"
#BACKGROUND_COLOR = "lightcyan"

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
    print("Forth dictionary saved.")
    messagebox.showinfo("Save", "Forth dictionary saved successfully.")
  
# ---------------------------- FUNCTION: PEEK_NUMBER -----------------------#
def peek_number():
    l = len(word_stack)
    if l == 0:
        return -1
    try:
        int_val = int(word_stack[l -1])
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

# ---------------------------- FUNCTION: ENTER -----------------------#
def enter():
    global word_stack
    command = input_text.get().strip()
    if command == "bye":
        exit(0)
    elif command == "+" or command == "-" or command == "*" or command == "/" or command =="mod":
        op1 = pop_number()
        if op1  == -1:
            return
        op2 = pop_number()
        if op2  == -1:
            return
        result = op_eval (op1,op2, command)
        if command != -1:
           word_stack.append(str(result))
    else:
        word_stack.append(command)
    write_stack()
    input_text.delete(0, END)

# ---------------------------- FUNCTION: WRITE_MESSAGE-----------------#
def write_message():
    global data_message_text
    data_message_var.set(data_message_text)

# ---------------------------- FUNCTION: WRITE_STACK -----------------#
def write_stack():
    global data_stack_text
    data_stack_text = str(word_stack)
    data_stack_var.set(data_stack_text)

# ---------------------------- FUNCTION: WRITE_PROMPT -----------------#
def write_prompt():
    global data_prompt_text
    data_prompt_var.set(data_prompt_text)

# ---------------------------- UI SETUP ------------------------------- #
word_stack = []
load_forth_dict()  # Load the initial stack from the JSON file

# --------------------------- MAIN -------------------------------------#
window = Tk()
window.title("Forth Interpreter")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

# label var
data_stack_text =str(word_stack)
data_message_text = ""
data_prompt_text = "ok>"
data_stack_var = StringVar()
data_message_var = StringVar()
data_prompt_var = StringVar()
data_stack_var.set(data_stack_text)
data_message_var.set(data_message_text)
data_prompt_var.set(data_prompt_text)

# canvas
canvas = Canvas(window, height=300, width=400, bg=BACKGROUND_COLOR, highlightthickness=0)
canvas.grid(row=0, column=0, columnspan=2, padx=20,pady=20)

#Text in canvas
stack_label = Label(canvas, text="stack", fg="black", bg=BACKGROUND_COLOR)
stack_label.grid(row=0,column=0)
input_label = Label(canvas, text="input",fg="black", bg=BACKGROUND_COLOR)
input_label.grid(row=1,column=0)
message_label = Label(canvas, text="message", fg="black", bg=BACKGROUND_COLOR)
message_label.grid(row=2,column=0)


stack_text = Label(canvas, font=("Ariel", 14), textvariable=data_stack_var, fg="black", bg=BACKGROUND_COLOR)
stack_text.grid(row=0,column=1,columnspan=2)
prompt_text = Label(canvas, font=("Ariel", 16, "bold"), textvariable=data_prompt_var, fg="black", bg=BACKGROUND_COLOR)
prompt_text.grid(row=1,column=1)
input_text = Entry(canvas, font=("Ariel", 16, "italic"), fg="black", bg=BACKGROUND_COLOR)
input_text.grid(row=1,column=2)
message_text = Label(canvas,font=("Ariel", 14), textvariable=data_message_var, fg="black", bg=BACKGROUND_COLOR)
message_text.grid(row=2,column=1)

#Buttons
button_command = Button(canvas, text="<Enter word>", highlightthickness=0, command=enter)
button_command.grid(row=3, column=1)
button_command = Button(canvas, text="<Save stack>", highlightthickness=0, command=save_forth_dict)
button_command.grid(row=3, column=2)

window.mainloop()