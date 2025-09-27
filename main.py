from tkinter import *
from wordbank import words_list

window = Tk()
window.title("Typing Speed Application")

wpm_var = StringVar(value="WPM: 0")
wpm = Label(window, textvariable=wpm_var, font=("Courier", 20))
wpm.grid(row=0, column=0, sticky="w", padx=6, pady=6)

time_var = StringVar(value="Time left: 60")
time = Label(window, textvariable=time_var, font=("Courier", 20))
time.grid(row=0, column=1)

button = Button(window, text="Restart", font=("Courier", 20), command=None)
button.grid(row=0, column=2)

word_canvas = Canvas(width=150, height=300)
word_text = word_canvas.create_text(75, 150, text="word")
word_canvas.grid(row=1, column=0, columnspan=3)

placeholder = "Type the words here"
word_var = StringVar(value=placeholder)
entry = Entry(window, textvariable=word_var, font=("Courier", 20), width=60, justify="center", fg="gray")
entry.grid(row=2, column=0, columnspan=3, padx=5, pady=5)

window.mainloop()