#  mixer is a module from pygame that plays music
#  event is a module that enables us to use events such as mouse hold
#  Tk creates main window
#  Label, Button etc.. are just ui elements
#  subprocess enables cmd console for us to work with ffmpeg utility

from pygame import mixer, event
from tkinter import Tk, Label, Button, Scale, filedialog
from os import chdir
from datetime import timedelta
from subprocess import run

current_volume = float(0.5)
current_track_title = ""
current_track_path = ""
track_duration = 0
is_playing = False


#  utility functions


def know_track_duration(path_to_track):
    global current_track_title
    #  making path to track clean
    path_to_track = path_to_track.split("/")
    del path_to_track[-1]
    path_to_track = '/'.join(path_to_track)
    #  --------------------------
    try:
        process = run(f'ffprobe -v quiet -show_entries format=duration -of default=noprint_wrappers=1 {current_track_title}', shell=True, capture_output=True, text=True, cwd=path_to_track)
        duration = process.stdout.split("=")  #  this is gonna be something like duration=370.00032
        duration = duration[-1]
        duration = int(float(duration))
        return duration
    except Exception as e:
        print(e)


#  functions


def select_track():
    global current_track_title
    global current_track_path
    global track_duration
    global is_playing

    try:
        file_path = filedialog.askopenfilename(initialdir="C:/")
        if file_path == "":
            return
        current_track_path = file_path
        current_track_title = file_path.split("/")  # divided the whole directory into pieces by "/" symbol and placed  them in list
        current_track_title = current_track_title[-1]  # took the last element of the list (name of track actually)
        Track_being_played.config(text="Now playing:\n" + str(current_track_title))
        track_duration = know_track_duration(file_path)

        Music_Slider.config(to=track_duration)  #  giving our music slider the right length
        Music_Slider.set(0)

        Track_length_hms_label.config(text=f"{timedelta(seconds=track_duration)}")
        Pause_resume_button.config(text="^", command=play)

        mixer.init()
        mixer.music.load(current_track_path)
        mixer.music.set_volume(Volume_Slider.get())
    except Exception as e:
        print(e)

#  gotta edit this trio


def play():
    global is_playing
    is_playing = True

    Pause_resume_button.config(text="=", command=pause)
    try:
        mixer.music.play(start=Music_Slider.get())
    except Exception as e:
        print(e)


def pause():
    global is_playing
    is_playing = False

    Pause_resume_button.config(text="^", command=resume)
    try:
        mixer.music.pause()
    except Exception as e:
        print(e)


def resume():
    global is_playing
    is_playing = True

    Pause_resume_button.config(text="=", command=pause)
    try:
        mixer.music.play(start=Music_Slider.get())
    except Exception as e:
        print(e)


def manipulate_volume(curr_volume):
    try:
        mixer.music.set_volume(Volume_Slider.get())
    except Exception as e:
        print(e)


def manipulate_track_time(curr_time):
    global is_playing
    if is_playing:
        mixer.music.play(start=Music_Slider.get())
    else:
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

Pause_resume_button = Button(master, text="^", command=play)
Pause_resume_button.grid(row=4)

# Sliders
Music_Slider = Scale(master, orient="horizontal", length=330, from_=0, resolution=1, repeatdelay=0)
Music_Slider.bind('<ButtonRelease-1>', manipulate_track_time)
Music_Slider.grid(row=5)

Volume_Slider = Scale(master, orient="horizontal", length=80, from_=0, to=1, resolution=0.01, command=manipulate_volume)
Volume_Slider.grid(row=6)
Volume_Slider.set(current_volume)


# Labels
Track_being_played = Label(master, text="", bg="#ffffff")
Track_being_played.grid(row=7)

Track_length_hms_label = Label(master, text="0:00:00", bg="#ffffff")
Track_length_hms_label.grid(row=8)

Time_passed_label = Label(master, text="0:00:00", bg="#ffffff")
Time_passed_label.grid(row=9)

master.mainloop()  # we need to use this function, in order to constantly keep our window ready
