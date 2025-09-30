from tkinter import *
from tkinter import ttk
from tkinter import font as tkfont
from wordbank import words_list

# TO:DO
# 2. Set a countdown and only allows user to enter word when the time is running
# 3. Counts number of words correct in that time
# 4. Messagebox to show the WPM
# 5. Restart button

 
GAME_OVER = False
timer_started = False

# a set is used to prevent duplicates
matched = set()  # indices of words_list that have been correctly typed
current_index = 0

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
    
def check_word(event=None):
    global current_index

    typed = entry.get().strip()
    if not typed or typed == placeholder:
        return
    
    target = words_list[current_index]
    if typed.lower() == target.lower():
        matched.add(current_index)
        word_canvas.itemconfig(f"word-{current_index}", fill="green")

        current_index += 1
        if current_index < len(words_list):
            word_canvas.itemconfig(f"word-{current_index}", fill="blue")
        else : # finished all words in word list
            pass

    entry.delete(0, "end")
 
def countdown(count):
    time_var.set(f"Time left: {count}")

    if count > 0:
        window.after(1000, countdown, count-1)
        timer_started

def start_countdown_on_key_press(event):
    global timer_started
    
    if timer_started:
        return
    else :
        timer_started = True
        countdown(60)

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

# Creates a reusable Font object 
txt_font = tkfont.Font(family="Helvetica", size=20)

def redraw(event=None):
    margin = 10
    x = margin
    y = margin

    space_w = txt_font.measure(" ") # spacing between words
    line_h = txt_font.metrics("linespace") + 6
    max_w = max(word_canvas.winfo_width() - margin, 1)

    for i, w in enumerate(words_list):
        w_w = txt_font.measure(w) # the pixel width of the word w 
        # wrap to next line if this word would exceed the right edge
        if x + w_w > max_w:
            x = margin
            y += line_h
        
        if i in matched:
            color = "green"
        elif i == current_index:
            color = "blue"
        else:
            color = "black"

        word_canvas.create_text(
            x, y,
            text=w,
            font=txt_font,
            anchor="nw",
            fill=color,
            tags=(f"word-{i}", "word"),
        )
        x += w_w + space_w


placeholder = "Type the words here"
word_var = StringVar(value=placeholder)
entry = Entry(window, textvariable=word_var, font=("Courier", 20), width=60, justify="center", fg="gray")
entry.grid(row=3, column=0, columnspan=3, padx=5, pady=5)
entry.bind("<FocusIn>", focus_in)
entry.bind("<FocusOut>", focus_out)
entry.focus_set() # put cursor in box immediately

window.bind_all("<Button>", clear_focus_on_click)

word_canvas.bind("<Configure>", redraw)

entry.bind("<Return>", check_word)
entry.bind("<space>", check_word)

window.bind("<Key>", start_countdown_on_key_press)

window.mainloop()