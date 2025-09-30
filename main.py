from tkinter import *
from tkinter import ttk
from tkinter import font as tkfont
from wordbank import words_list_1, words_list_2, words_list_3, words_list_4, words_list_5
import random

current_index = 0
timer_started = False
timer_after = None
COUNTDOWN = 60
remaining_time = COUNTDOWN

# a set is used to prevent duplicates
matched = set()  # indices of words_list that have been correctly typed
all_correct_words_typed = []
all_words_typed = [] # all the words that have been typed, regardless of if it's correct or not
last_attempt = {}  # current_index : last wrong attempt

last_list_idx = None

all_words_list = [words_list_1, words_list_2, words_list_3, words_list_4, words_list_5]

def pick_new_words_list(avoid_idx=None):
    indices = list(range(len(all_words_list)))
    if avoid_idx is not None and avoid_idx in indices and len(indices) > 1:
        indices.remove(avoid_idx)
    idx = random.choice(indices)
    base = all_words_list[idx]
    wl = base[:]
    random.shuffle(wl)
    return idx, wl

last_list_idx, words_list = pick_new_words_list(avoid_idx=None)

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
    
    all_words_typed.append(typed.lower())

    target = words_list[current_index]
    if typed.lower() == target.lower():
        matched.add(current_index)
        all_correct_words_typed.append(typed.lower())
        word_canvas.itemconfig(f"word-{current_index}", fill="green")

        current_index += 1
        if current_index < len(words_list):
            word_canvas.itemconfig(f"word-{current_index}", fill="blue")
        wpm_var.set(f"WPM: {calculate_wpm()}")       
    else :
        last_attempt[current_index] = typed.lower()
        word_canvas.itemconfig(f"word-{current_index}", fill="red")

        current_index += 1
        if current_index < len(words_list):
            word_canvas.itemconfig(f"word-{current_index}", fill="blue")
        wpm_var.set(f"WPM: {calculate_wpm()}")  

    entry.delete(0, "end")
    return "break"  

def edit_word(event):
    global current_index

    if entry.get() == "" and current_index > 0 and current_index-1 in last_attempt:
        word_canvas.itemconfig(f"word-{current_index}", fill="black")
        current_index -= 1
        word_canvas.itemconfig(f"word-{current_index}", fill="blue")
        entry.insert(0, last_attempt[current_index])
        entry.icursor("end")

def countdown():
    global remaining_time, timer_after

    time_var.set(f"Time left: {remaining_time}")

    if remaining_time > 0:
        remaining_time -= 1      
        timer_after = window.after(1000, countdown)
    else:
        wpm_var.set(f"WPM: {calculate_wpm()}")       
        entry.config(state="disabled")   
        timer_after = None 

def start_countdown_on_key_press(event):
    global timer_started, remaining_time
    
    if timer_started:
        return
    else :
        timer_started = True
        remaining_time = COUNTDOWN
        countdown()
        wpm_var.set(f"WPM: {calculate_wpm()}")

def calculate_wpm():
    time_elapsed = COUNTDOWN - remaining_time
    if time_elapsed <= 0:
        return 0
    time_in_mins = time_elapsed / 60

    total_chars = sum(len(words_list[i]) for i in matched)
    wpm = (total_chars / 5) / time_in_mins

    return int(wpm)    

def restart():
    global current_index, timer_started, timer_after, remaining_time
    global matched, all_correct_words_typed, all_words_typed, last_attempt
    global last_list_idx, words_list

    if timer_after is not None:
        window.after_cancel(timer_after)
        timer_after = None

    current_index = 0
    timer_started = False
    remaining_time = COUNTDOWN
    matched = set()  
    all_correct_words_typed = []
    all_words_typed = [] 
    last_attempt = {} 

    last_list_idx, words_list = pick_new_words_list(avoid_idx=last_list_idx)

    wpm_var.set(value="WPM: 0")
    time_var.set(value=f"Time left: {remaining_time}")
    entry.config(state="normal", fg="gray")
    entry.delete(0, "end")
    entry.insert(0, placeholder)
    entry.focus_set() 

    word_canvas.delete("all")
    redraw()

window = Tk()
window.title("Typing Speed Application")

wpm_var = StringVar(value="WPM: 0")
wpm = Label(window, textvariable=wpm_var, font=("Courier", 20))
wpm.grid(row=0, column=0, padx=6, pady=6)

time_var = StringVar(value=f"Time left: {remaining_time}")
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

window.bind_all("<Button>", clear_focus_on_click)

entry.bind("<Return>", check_word)
entry.bind("<space>", check_word)

window.bind("<Key>", start_countdown_on_key_press)

entry.bind("<KeyRelease-BackSpace>", edit_word)

entry.focus_set() # put cursor in box immediately
word_canvas.bind("<Configure>", redraw)

window.mainloop()