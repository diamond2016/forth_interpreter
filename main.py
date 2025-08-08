from tkinter import *
from tkinter import messagebox
import random
import json
import os


#BACKGROUND_COLOR = "#B1DDC6"
BACKGROUND_COLOR = "lightcyan"

# ---------------------------- FUNCTION: LOAD_WORD_DICT -----------------------#
def load_word_dict_list():
    #se esiste file_name="word_to_learn.json" altrimenti "french_word.json" (in data)
    if os.path.exists("data/words_to_learn.json"):
        file_name = "data/words_to_learn.json"
    else:
        file_name = "data/french_words.json"
    
    with open(file_name,"r") as file:
        dict = json.load(file)
        return dict["words"]

# ---------------------------- FUNCTION: WRITE_WORD_DICT -----------------------#
def write_word_dict_list(file_name):
    with open(file_name,"w") as file:
        new_dict = {"words": word_dict_list}
        json.dump(new_dict, file)
        print(f"creato nuovo file parole {file_name}")
 
# ---------------------------- FUNCTION: PEEK_NUMBER -----------------------#
def peek_number():
    l = len(word_stack)
    if l == 0:
        return -1
    try:
        intval = int(word_stack[l -1])
    except ValueError:
        return -1
    else:
        return intval
# ---------------------------- FUNCTION: POP_NUMBER ------------------------#
def pop_integer():
    intval = peek_number()
    if intval != -1:
        word_stack.pop()   
    return intval
 
# ---------------------------- FUNCTION: ENTER -----------------------#
def enter():
    command = input_text.get().strip()
    if command == "bye":
        exit(0)
    elif command == "+":
        op1 = pop_integer()
        if (op1  == -1):
            return
        op2 = pop_integer()
        if (op1  == -1):
            return
        result = op1 + op2
        word_stack.append(str(result))
    else:
        word_stack.append(command)
    write_stack()
    input_text.delete(0, END)

# ---------------------------- FUNCTION: WRITE_MESSAGE-----------------#
def write_message():
    data_message_var.set(data_message_text)

# ---------------------------- FUNCTION: WRITE_STACK -----------------#
def write_stack():
    data_stack_text = str(word_stack)
    data_stack_var.set(data_stack_text)
    
# ---------------------------- FUNCTION: WRITE_PROMPT -----------------#
def write_prompt():
    data_prompt_var.set(data_prompt_text)

# ---------------------------- UI SETUP ------------------------------- #
word_stack = []

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


canvas = Canvas(window, height=300, width=400, bg=BACKGROUND_COLOR, highlightthickness=0)
canvas.grid(row=0, column=0, columnspan=2, padx=20,pady=20)

#Text in canvas
stack_label = Label(canvas, text="stack", fg="black", bg=BACKGROUND_COLOR)
stack_label.grid(row=0,column=0)
input_label = Label(canvas, text="input",fg="black", bg=BACKGROUND_COLOR)
input_label.grid(row=1,column=0)
message_label = Label(canvas, text="message", fg="black", bg=BACKGROUND_COLOR)
message_label.grid(row=2,column=0)

#stack_text = language_text = canvas.create_text(100,50, anchor="center", font=("Ariel", 30, "italic"), text=data_stack_text, fill="black")
stack_text = Label(canvas, font=("Ariel", 14), textvar=data_stack_var, fg="black", bg=BACKGROUND_COLOR)
stack_text.grid(row=0,column=1,columnspan=2)
prompt_text = Label(canvas, font=("Ariel", 16, "bold"), textvar=data_prompt_var, fg="black", bg=BACKGROUND_COLOR)
prompt_text.grid(row=1,column=1)
input_text = Entry(canvas, font=("Ariel", 16, "italic"), text="input text", fg="black", bg=BACKGROUND_COLOR)
input_text.grid(row=1,column=2)
message_text = Label(canvas,font=("Ariel", 14), textvar=data_message_var, fg="black", bg=BACKGROUND_COLOR)
message_text.grid(row=2,column=1)

#Button
button_command = Button(canvas, text="<Enter command input>", highlightthickness=0, command=enter)
button_command.grid(row=2, column=1, columnspan=2)

window.mainloop()