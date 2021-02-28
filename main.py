from pygame import mixer  # mixer is going to be used as module that manipulates audio files (playing, pausing etc..)
from tkinter import Tk
from tkinter import Label  # interface element label
from tkinter import Button  # interface element button
from tkinter import Scale  # gives us slider element
from tkinter import filedialog  # module for file management (choosing a track essentially)

current_volume = float(0.5)
current_track_title = ""
current_track_path = ""
current_play_time = float(0.0)
# Functions


def select_track():
    global current_track_title
    global current_track_path
    filename = filedialog.askopenfilename(initialdir="C:/")
    current_track_path = filename
    current_track_title = filename.split("/")  # divided the whole directory into pieces by "/" symbol and placed in them in list
    current_track_title = current_track_title[-1]  # took the last element of the list (name of track actually)


def play():
    Pause_resume_button.config(text="pause", command=pause)
    try:
        mixer.init()
        mixer.music.load(current_track_path)
        mixer.music.set_volume(current_volume)
        mixer.music.play()
        Track_being_played.config(text="Now playing:\n" + str(current_track_title))
    except Exception as e:
        print(e)


def pause():
    try:
        Pause_resume_button.config(text="resume", command=resume)
        mixer.music.pause()
    except Exception as e:
        print(e)

def resume():
    pass

# Main Screen
master = Tk()  # creating the main window
master.title("Ultimate Music Player")  # assigning a name to our main window (program)
master['bg'] = "#FFFFFF"  # setting white background color for main  window
master.geometry('600x600')
master.resizable(False, False)

# Images

# Buttons
Select_track_button = Button(master, text="Select track", command=select_track)
Select_track_button.grid(row=1)

Skip_forward_button = Button(master, text=">>")
Skip_forward_button.grid(row=2)

Skip_backwards_button = Button(master, text="<<")
Skip_backwards_button.grid(row=3)

Pause_resume_button = Button(master, text="play", command=play)
Pause_resume_button.grid(row=4)

# Sliders
Music_Slider = Scale(master, )
Music_Slider.grid(row=5)

Volume_Slider = Scale(master, )
Volume_Slider.grid(row=6)

# Labels
Track_being_played = Label(master, text="")
Track_being_played.grid(row=7)

master.mainloop()  # we need to use this function, in order to constantly keep our window ready
