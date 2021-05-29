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
autoplay = 0
media_filetypes = [('media files', ('*.mp3', '*.flac', '*.ogg', '*.wav'))]


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
        for track_title in selected_tracks:
            track_title = (track_title.split('/'))[-1]
            Track_box.insert(END, track_title)
        mixer.init()
        Music_Slider.config(state=ACTIVE)

    except Exception as e:
        print(e)


def play():
    global is_playing
    global current_track_title
    global current_tracks_path
    is_playing = True
    Pause_resume_button.config(text="pause", command=pause)
    try:
        mixer.music.play(start=Music_Slider.get())
        update_music_slider_position()
    except Exception as e:
        print(e)


def replay():
    Pause_resume_button.config(text="replay", command=pause)
    Music_Slider.set(0)
    play()


def pause():
    global is_playing
    global after_id
    is_playing = False
    Pause_resume_button.config(text="play", command=play)
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
    mixer.music.load(current_tracks_path + "/" + current_track_title)
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


def next_track():
    global current_track_title

    index = Track_box.get(0, "end").index(current_track_title)
    Track_box.selection_clear(0, "end")

    if Track_box.size() == index + 1:
        Track_box.activate(0)
        Track_box.selection_set(0)
        play_selected_track()
        return

    Track_box.activate(index+1)
    Track_box.selection_set(index+1)
    play_selected_track()


def prev_track():
    global current_track_title

    index = Track_box.get(0, "end").index(current_track_title)
    Track_box.selection_clear(0, "end")

    if index == 0:
        Track_box.activate(Track_box.size() - 1)
        Track_box.selection_set(Track_box.size() - 1)
        play_selected_track()
        return

    Track_box.activate(index - 1)
    Track_box.selection_set(index-1)
    play_selected_track()




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
    global autoplay
    if autoplay & (Music_Slider.get() == track_duration):

        index = Track_box.get(0, "end").index(current_track_title)
        Track_box.selection_clear(0, "end")
        if Track_box.size() != index + 1:
            Track_box.activate(index+1)
            Track_box.selection_set(index+1)
            play_selected_track()
            return
        else:
            Track_box.activate(0)
            Track_box.selection_set(0)
            play_selected_track()
            return
    elif Music_Slider.get() == track_duration:
        Pause_resume_button.config(text="replay", command=replay)
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
    global autoplay
    Time_passed_label.config(text=timedelta(seconds=int(x)))
    if autoplay & (int(x) == track_duration):

        index = Track_box.get(0, "end").index(current_track_title)
        Track_box.selection_clear(0, "end")
        if Track_box.size() != index + 1:
            Track_box.activate(index + 1)
            Track_box.selection_set(index + 1)
            play_selected_track()
            return
        else:
            Track_box.activate(0)
            Track_box.selection_set(0)
            play_selected_track()
            return
    elif int(x) == track_duration:
        Pause_resume_button.config(text="replay", command=replay)
        Time_passed_label.after_cancel(after_id)
        is_playing = False


def scrollbar_mouse_control():
    Playlist_scrollbar.set()


def enable_autoplay():
    global autoplay
    if autoplay:
        autoplay = False
    else:
        autoplay = True


# Main Screen
master = Tk()  # creating the main window
master.title("Ultimate Music Player")  # assigning a name to our main window (program)
master['bg'] = "#FFFFFF"  # setting white background color for main  window
master.geometry('450x450')
master.resizable(False, False)


# Images

play_img = PhotoImage(file='Source images/play_button.png')
pause_img = PhotoImage(file='Source images/pause_button.png')
replay_img = PhotoImage(file='Source images/replay_button.png')
skip_time_button_f_img = PhotoImage(file='Source images/skip_time_button.gif')
skip_time_button_img = PhotoImage(file='Source images/skip_time_button_left.gif')
next_track_button_img = PhotoImage(file='Source images/next_track.gif')
prev_track_button_img = PhotoImage(file='Source images/prev_track.gif')


# Creating and packing frames

Main_bottom_frame = Frame(master, bg='#ffffff')
Main_bottom_frame.pack(side=BOTTOM, pady=10)

Volume_slider_frame = Frame(Main_bottom_frame, bg="#ffffff")
Volume_slider_frame.pack(fill=X)

Track_being_played = Label(master, bg="#ffffff")
Track_being_played.pack(side=BOTTOM)

Control_buttons_frame = Frame(Main_bottom_frame, bg='#ffffff')
Control_buttons_frame.pack(side=BOTTOM)

Track_time_frame = Frame(Main_bottom_frame, bg="#ffffff")
Track_time_frame.pack(fill=X, side=BOTTOM)

Playlist_frame = Frame(master,bg="#ffffff")
Playlist_frame.pack(fill=X, padx=20)


# Play list menu

#Playlist_scrollbar = Scrollbar(Playlist_frame, troughcolor="#ffffff", bg="#000000", activebackground="#0F031D")
new_slider = Scale(Playlist_frame, length=150,showvalue=0, activebackground="#000000" ,troughcolor="#ffffff", bg="#000000",from_=0, to=10, resolution=1, orient = VERTICAL)
Track_box = Listbox(Playlist_frame,selectbackground="#C0C0C0", bd=5, fg="#000000", selectmode=SINGLE, bg='white', width=100)#, yscrollcommand=new_slider.set)
Track_box.bind('<<ListboxSelect>>', show_action)
new_slider.config(command=Track_box.yview)
#Playlist_scrollbar.config(command=Track_box.yview)


# Checkbox

autoplay_checkbox = Checkbutton(master, text="Autoplay", bg="#ffffff",variable=autoplay, onvalue=True, offvalue=False, command=enable_autoplay)
autoplay_checkbox.pack()

# Buttons

Select_track_button = Button(Playlist_frame, bg="#000000", fg="#ffffff", activebackground="#000000", bd=7,
                             width=40, height=1,
                             text="Select tracks", font="Verdana 10", command=select_tracks)


Select_new_track_button = Button(Playlist_frame, bg="#000000", fg="#ffffff", activebackground="#000000", bd=7,
                             text="play selected", command=play_selected_track)

Skip_forward_button = Button(Control_buttons_frame, bg="#000000", fg="#ffffff", activebackground="#000000", bd=7,
                             width=6, height=1,
                             text=">>", font="Verdana 10", command=skip_forward)

Skip_backwards_button = Button(Control_buttons_frame, bg="#000000", fg="#ffffff", activebackground="#000000", bd=7,
                             width=6, height=1,
                             text="<<", font="Verdana 10", command=skip_backwards)

Next_track_button = Button(Control_buttons_frame, bg="#000000", fg="#ffffff", activebackground="#000000", bd=7,
                             width=6, height=1,
                             text=">", font="Verdana 10", command=next_track)

Previous_track_button = Button(Control_buttons_frame, bg="#000000", fg="#ffffff", activebackground="#000000", bd=7,
                             width=6, height=1,
                             text="<", font="Verdana 10", command=prev_track)

Pause_resume_button = Button(Control_buttons_frame, bg="#000000", fg="#ffffff", activebackground="#000000", bd=7,
                             width=6, height=1, font="Verdana 10",
                             text="play",command=play)


# Sliders

Music_Slider = Scale(Main_bottom_frame, state=DISABLED, orient="horizontal",
                     troughcolor="#ffffff", bg="#000000", resolution=1, repeatdelay=1, showvalue=False,
                     length=330, from_=0, activebackground="#000000", command=slideOfmusicSlider)
Music_Slider.bind('<ButtonRelease-1>', manipulate_track_time)
Music_Slider.bind('<ButtonPress-1>', stop_while_manipulating)

Volume_Slider = Scale(Volume_slider_frame, orient="horizontal", bg="#000000", troughcolor="#ffffff",
                      showvalue=False, activebackground="#000000",
                      length=80, from_=0, to=1, resolution=0.01, command=manipulate_volume)
Volume_Slider.set(current_volume)
Volume_Slider.pack(side=RIGHT)

# Labels

Track_length_hms_label = Label(Track_time_frame, bg="#ffffff", text="0:00:00")

Time_passed_label = Label(Track_time_frame, bg="#ffffff", text="0:00:00")

# Packing widgets into frames
Select_track_button.pack(pady=10)

#Playlist_scrollbar.pack(side=RIGHT,fill=Y)
new_slider.pack(side=RIGHT, fill=Y)

Track_box.pack(padx=20)
Select_new_track_button.pack(fill=X, padx=20)

Music_Slider.pack(side=TOP)

Previous_track_button.pack(side=LEFT)
Skip_backwards_button.pack(side=LEFT)
Pause_resume_button.pack(side=LEFT)
Skip_forward_button.pack(side=LEFT)
Next_track_button.pack(side=LEFT)


Time_passed_label.pack(side=LEFT)
Track_length_hms_label.pack(side=RIGHT)

master.mainloop()  # we need to use this method, in order to constantly keep our window ready
