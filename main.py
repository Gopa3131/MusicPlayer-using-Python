#  mixer is a module from pygame that plays music
#  event is a module that enables us to use events such as mouse hold
#  Tk creates main window
#  Label, Button etc.. are just ui elements
#  subprocess enables cmd console for us to work with ffmpeg utility

from pygame import mixer

from tkinter import Tk, Label, Button, Scale, filedialog
from tkinter import *

from datetime import timedelta

from subprocess import run
from os import path

current_volume = float(0.5)
current_track_title = ""
current_tracks_path = ""
track_duration = 0
is_playing = False
after_id = 0
media_filetypes = [('media files', ('*.mp3', '*.mp4', '*.flac', '*.ogg', '*.wav', '*.ape', '*.au', '*.aiff'))]



#  utility functions


def know_track_duration(path_to_track):
    global current_track_title
    try:
        process = run(f'ffprobe -v quiet -show_entries format=duration -of default=noprint_wrappers=1 "{current_track_title}"', shell=True, capture_output=True, text=True, cwd=path_to_track)
        duration = process.stdout.split("=")  #  this is gonna be something like duration=370.00032
        duration = duration[-1]
        duration = int(float(duration))
        return duration
    except Exception as e:
        print(e)


#  interface functions


def select_tracks():
    global current_tracks_path
    try:
        selected_tracks = filedialog.askopenfilenames(initialdir="C:/", filetypes=media_filetypes)
        if not selected_tracks:
            return
        else:
            Track_box.delete(0, END)
        current_tracks_path = (path.split(selected_tracks[0]))[0]
        print("---" + current_tracks_path)
        for track_title in selected_tracks:
            track_title = (track_title.split('/'))[-1]
            Track_box.insert(END, track_title)
        mixer.init()

    except Exception as e:
        print(e)


def play():
    global is_playing
    global current_track_title
    global current_tracks_path
    is_playing = True
    Pause_resume_button.config(text="=", command=pause)
    try:
        mixer.music.play(start=Music_Slider.get())
        update_music_slider_position()
    except Exception as e:
        print(e)


def replay():
    Pause_resume_button.config(text="=", command=pause)
    Music_Slider.set(0)
    play()


def pause():
    global is_playing
    global after_id
    is_playing = False
    Pause_resume_button.config(text="^", command=play)
    try:
        Time_passed_label.after_cancel(after_id)
        mixer.music.stop()
    except Exception as e:
        print(e)


def show_action(event):
    pass


def play_selected_track():
    global current_track_title
    global track_duration
    global after_id
    mixer.music.stop()
    mixer.music.unload()
    try:
        Time_passed_label.after_cancel(after_id)
    except Exception as e:
        print(e)
    current_track_title = Track_box.get(ACTIVE)
    track_duration = know_track_duration(current_tracks_path)
    Track_length_hms_label.config(text=timedelta(seconds=track_duration))
    Music_Slider.config(to=track_duration)
    Music_Slider.set(0)
    Time_passed_label.config(text="0:00:00")
    Track_being_played.config(text=current_track_title)
    mixer.music.load(current_tracks_path + current_track_title)
    play()

def skip_forward():
    global is_playing
    if is_playing:
        is_playing = False
        Time_passed_label.after_cancel(after_id)
        current_pos = Music_Slider.get()
        mixer.music.stop()
        Music_Slider.set(current_pos + 4)
        play()
    else:
        current_pos = Music_Slider.get()
        Music_Slider.set(current_pos + 5)


def skip_backwards():
    global is_playing
    if is_playing:
        is_playing = False
        Time_passed_label.after_cancel(after_id)
        current_pos = Music_Slider.get()
        mixer.music.stop()
        if current_pos <= 5:
            Music_Slider.set(0)
        else:
            Music_Slider.set(current_pos-6)
        play()
    else:
        current_pos = Music_Slider.get()
        if current_pos <= 5:
            Music_Slider.set(0)
        else:
            Music_Slider.set(current_pos - 5)


def update_music_slider_position():
    global is_playing
    global after_id
    current_song_position = Music_Slider.get()
    if is_playing:
        after_id = Time_passed_label.after(1000, update_music_slider_position)
        Music_Slider.set(current_song_position + 1)


def manipulate_volume(x):
    try:
        mixer.music.set_volume(Volume_Slider.get())
    except Exception as e:
        print(e)


def manipulate_track_time(curr_time):
    global is_playing
    if Music_Slider.get() == track_duration:
        Pause_resume_button.config(text="↺", command=replay)
        Time_passed_label.after_cancel(after_id)
        is_playing = False
    if is_playing:
        play()


def stop_while_manipulating(x):
    global after_id
    if is_playing:
        Time_passed_label.after_cancel(after_id)
        mixer.music.stop()


def slideOfmusicSlider(x):
    global after_id
    Time_passed_label.config(text=timedelta(seconds=int(x)))
    if int(x) == track_duration:
        is_playing = False
        Pause_resume_button.config(text="↺", command=replay)
        Time_passed_label.after_cancel(after_id)


# Main Screen
master = Tk()  # creating the main window
master.title("Ultimate Music Player")  # assigning a name to our main window (program)
master['bg'] = "#FFFFFF"  # setting white background color for main  window
master.geometry('450x450')
master.resizable(False, False)

# Creating and packing frames

Main_bottom_frame = Frame(master)
Main_bottom_frame.pack(side=BOTTOM, pady=10)

Volume_slider_frame = Frame(Main_bottom_frame)
Volume_slider_frame.pack(fill=X)

Track_being_played = Label(master, bg="#ffffff")
Track_being_played.pack(side=BOTTOM)

Control_buttons_frame = Frame(Main_bottom_frame)
Control_buttons_frame.pack(side=BOTTOM)

Track_time_frame = Frame(Main_bottom_frame)
Track_time_frame.pack(fill=X, side=BOTTOM)

Playlist_frame = Frame(master)
Playlist_frame.pack(fill=X, padx=20)


# Play list menu

Playlist_scrollbar = Scrollbar(Playlist_frame)
Track_box = Listbox(Playlist_frame, bg='purple', fg='white', width=100, yscrollcommand=Playlist_scrollbar.set)
Track_box.bind('<<ListboxSelect>>', show_action)


# Buttons

Select_track_button = Button(Playlist_frame, text="Select tracks", command=select_tracks)
Skip_forward_button = Button(Control_buttons_frame, text=">>", command=skip_forward)

Skip_backwards_button = Button(Control_buttons_frame, text="<<", command=skip_backwards)

Pause_resume_button = Button(Control_buttons_frame, text="^", command=play)

Select_new_track_button = Button(Playlist_frame, text="Play selected", command=play_selected_track)


# Sliders
Music_Slider = Scale(Main_bottom_frame, orient="horizontal", showvalue=False, length=330, from_=0, resolution=1, repeatdelay=0, command=slideOfmusicSlider)
Music_Slider.bind('<ButtonRelease-1>', manipulate_track_time)
Music_Slider.bind('<ButtonPress-1>', stop_while_manipulating)

Volume_Slider = Scale(Volume_slider_frame, orient="horizontal", showvalue=False ,length=80, from_=0, to=1, resolution=0.01, command=manipulate_volume)
Volume_Slider.set(current_volume)
Volume_Slider.pack(side=RIGHT)

# Labels

Track_length_hms_label = Label(Track_time_frame, text="0:00:00")

Time_passed_label = Label(Track_time_frame, text="0:00:00")

# Packing widgets into frames
Select_track_button.pack(pady=10)

Playlist_scrollbar.pack(side=RIGHT,fill=Y)

Track_box.pack(padx=20)
Select_new_track_button.pack(fill=X, padx=20)

Music_Slider.pack(side=TOP)

Skip_backwards_button.pack(side=LEFT, padx=10)
Pause_resume_button.pack(side=LEFT, padx=10)
Skip_forward_button.pack(side=LEFT,padx=10)

#Volume_Slider.pack(side=RIGHT,padx=20, ipady=6)

Time_passed_label.pack(side=LEFT)
Track_length_hms_label.pack(side=RIGHT)

master.mainloop()  # we need to use this function, in order to constantly keep our window ready
