# Wack a mole
import Tkinter as tk
import tkMessageBox as messagebox
import random
import winsound

# Global variables
win = tk.Tk()           # our main window
SIZE = 6                # the size of one side of the field
game_over = False
current_mole = None
hits_count = tk.IntVar(win) #set up the hit counter
miss_count = tk.IntVar(win) # Set up the miss counter
mole_timer = None

#load the mole image
mole_image = tk.PhotoImage(file="mole.gif", master=win)
blank_image = tk.PhotoImage(file="blank.gif", master=win)

#Set up the main window
win.title('WAM')
win.tk.call("wm", "iconphoto", win._w, mole_image)

def start_game():
    global current_mole, start_button, game_over

    start_button['state'] = tk.DISABLED

    hits_count.set(0)
    miss_count.set(0)
    
    game_over = False
    random_mole()
  
def random_mole():
    global current_mole, mole_timer

    if current_mole is not None:
        mole[current_mole]['image'] = blank_image
    
    current_mole = random.randrange(len(mole))
    mole[current_mole]['image'] = mole_image 

    if mole_timer is not None:
        win.after_cancel(mole_timer)
    if game_over is False:
        mole_timer = win.after(1000, missed)

def end_game():
    global current_mole, game_over

    game_over = True
    messagebox.showinfo("WAM", "Game Over!")
    start_button['state'] = tk.NORMAL
    mole[current_mole]['image'] = blank_image
    current_mole = None;
    
def smash(event):
    if current_mole is None:
        return

    if event.widget == mole[current_mole]:
        hits_count.set(hits_count.get() + 1)
        winsound.PlaySound("smash.wav", winsound.SND_FILENAME + winsound.SND_ASYNC)
        random_mole() 
    else:
        winsound.PlaySound("whiff.wav", winsound.SND_FILENAME + winsound.SND_ASYNC)
        missed_mole()
        
def missed_mole():
        miss_count.set(miss_count.get() + 1)

        if miss_count.get() == 3:
            end_game()

def missed():
    missed_mole()
    if current_mole is not None:
        random_mole()
    
    
#creat containers for my controls
field = tk.Frame(win)
controls = tk.Frame(win)

#add containers to the window
field.pack(side=tk.LEFT, padx=10, pady=10)
controls.pack(side=tk.LEFT, fill=tk.Y)

#add the display widgets
tk.Label(controls, text="Hits:").pack()
hits_label = tk.Label(controls, textvariable=hits_count)
hits_label.pack()

tk.Label(controls, text="Misses:").pack()
misses_label = tk.Label(controls, textvariable=miss_count)
misses_label.pack()

start_button = tk.Button(controls, text="Start")
start_button.pack()
start_button['command'] = start_game

#add the mole buttons
mole = []
for i in range(SIZE * SIZE):
    mole.append(tk.Label(field, image=blank_image, width=64, height=64))
    mole[i].grid(row=i/SIZE, column=i%SIZE)
    mole[i].bind("<Button-1>", smash)

# begin the event loop
win.mainloop()