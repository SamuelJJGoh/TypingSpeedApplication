from tkinter import *
from tkinter import ttk
from wordbank import words_list

def focus_in(event):
    if entry.get() == placeholder:
        entry.delete(0, "end")
        entry.config(fg="black")

def focus_out(event):
    if not entry.get().strip():
        entry.insert(0, placeholder)
        entry.config(fg="gray")

def clear_focus_on_click(event):
    if event.widget is not entry:
        window.focus_set() 

def on_canvas_resize(event):
    word_canvas.itemconfig(text_id, width=max(event.width - 20, 1))

def restart():
    pass

window = Tk()
window.title("Typing Speed Application")

wpm_var = StringVar(value="WPM: 0")
wpm = Label(window, textvariable=wpm_var, font=("Courier", 20))
wpm.grid(row=0, column=0, padx=6, pady=6)

time_var = StringVar(value="Time left: 60")
time = Label(window, textvariable=time_var, font=("Courier", 20))
time.grid(row=0, column=1)

button = Button(window, text="Restart", font=("Courier", 20), command=restart)
button.grid(row=0, column=2)

sep = ttk.Separator(window, orient="horizontal")
sep.grid(row=1, column=0, columnspan=3, sticky="ew", padx=5, pady=5)

word_canvas = Canvas(window, width=150, height=300, highlightthickness=0)
word_canvas.grid(row=2, column=0, columnspan=3, padx=5, pady=5, sticky="nsew")


text_id = word_canvas.create_text(
    10, 10,
    text=" ".join(words_list),
    anchor="nw",
    width=1,                    # temporary; we’ll set it after we know the size
    font=("Helvetica", 20),
    justify="left"
)

placeholder = "Type the words here"
word_var = StringVar(value=placeholder)
entry = Entry(window, textvariable=word_var, font=("Courier", 20), width=60, justify="center", fg="gray")
entry.grid(row=3, column=0, columnspan=3, padx=5, pady=5)
entry.bind("<FocusIn>", focus_in)
entry.bind("<FocusOut>", focus_out)
entry.focus_set() # put cursor in box immediately

window.bind_all("<Button>", clear_focus_on_click)

word_canvas.bind("<Configure>", on_canvas_resize)


window.mainloop()