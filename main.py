#  mixer is a module from pygame that plays music
#  event is a module that enables us to use events such as mouse hold
#  Tk creates main window
#  Label, Button etc.. are just ui elements
#  subprocess enables cmd console for us to work with ffmpeg utility

from pygame import mixer

from tkinter import Tk, Label, Button, Scale, filedialog, Canvas
from tkinter import *

from datetime import timedelta

from subprocess import run
from os import path


class MusicPlayer:
    def __init__(self):
        self.current_volume = float(0.5)
        self.current_track_title = ""
        self.current_tracks_path = ""
        self.track_duration = 0
        self.is_playing = False
        self.after_id = 0
        self.autoplay = 0
        self.media_filetypes = [('media files', ('*.mp3', '*.flac', '*.ogg', '*.wav'))]


        # Main Screen
        self.master = Tk()  # creating the main window
        self.master.title("Ultimate Music Player")  # assigning a name to our main window (program)
        self.master['bg'] = "#FFFFFF"  # setting white background color for main  window
        self.master.geometry('450x450')
        self.master.resizable(False, False)
        self.canvas = Canvas(self.master)
        self.canvas.pack()


        for i in range(0,100):
            self.canvas.create_line(10 * i, 0, 0, 10 * i, width=3, fill="red")


        # Images


        # Creating and packing frames

        self.Main_bottom_frame = Frame(self.canvas, bg='#ffffff')
        self.Main_bottom_frame.pack(side=BOTTOM, pady=10)

        self.Volume_Slider_frame = Frame(self.Main_bottom_frame, bg="#ffffff")
        self.Volume_Slider_frame.pack(fill=X)

        self.Track_being_played = Label(self.canvas, bg="#ffffff")

        self.Control_buttons_frame = Frame(self.Main_bottom_frame, bg='#ffffff')
        self.Control_buttons_frame.pack(side=BOTTOM)

        self.Track_time_frame = Frame(self.Main_bottom_frame, bg="#ffffff")
        self.Track_time_frame.pack(fill=X, side=BOTTOM)

        self.Playlist_frame = Frame(self.canvas, bg="#ffffff")
        self.Playlist_frame.pack(fill=X, padx=20, pady=20)

        # Play list menu

        # Playlist_scrollbar = Scrollbar(self.Playlist_frame, troughcolor="#ffffff", bg="#000000", activebackground="#0F031D")
        self.new_slider = Scale(self.Playlist_frame, state=DISABLED, length=150, showvalue=0, activebackground="#000000",
                           troughcolor="#ffffff", bg="#000000", from_=0, to=10, resolution=1, orient=VERTICAL)
        self.Track_box = Listbox(self.Playlist_frame, selectbackground="#C0C0C0", bd=5, fg="#000000", selectmode=SINGLE,
                            bg='white', width=100)
        self.new_slider.config(command=self.Track_box.yview)

        # Playlist_scrollbar.config(command=self.Track_box.yview)

        # Checkbox

        self.autoplay_checkbox = Checkbutton(self.canvas, text="autoplay", bg="#ffffff", variable=self.autoplay,
                                             onvalue=True, offvalue=False, command=self.enable_autoplay)
        self.autoplay_checkbox.pack()

        # Buttons

        self.Select_track_button = Button(self.Playlist_frame, bg="#000000", fg="#ffffff", activebackground="#000000", bd=7,
                                     width=40, height=1,
                                     text="Select tracks", font="Verdana 10", command=self.select_tracks)

        self.Select_new_track_button = Button(self.Playlist_frame, bg="#000000", fg="#ffffff", activebackground="#000000", bd=7,
                                         text="play selected", command=self.play_selected_track)

        self.Skip_forward_button = Button(self.Control_buttons_frame, bg="#000000", fg="#ffffff", activebackground="#000000",
                                     bd=7,
                                     width=6, height=1,
                                     text=">>", font="Verdana 10", command=self.skip_forward)

        self.Skip_backwards_button = Button(self.Control_buttons_frame, bg="#000000", fg="#ffffff", activebackground="#000000",
                                       bd=7,
                                       width=6, height=1,
                                       text="<<", font="Verdana 10", command=self.skip_backwards)

        self.Next_track_button = Button(self.Control_buttons_frame, bg="#000000", fg="#ffffff", activebackground="#000000", bd=7,
                                   width=6, height=1,
                                   text=">", font="Verdana 10", command=self.next_track)

        self.Previous_track_button = Button(self.Control_buttons_frame, bg="#000000", fg="#ffffff", activebackground="#000000",
                                       bd=7,
                                       width=6, height=1,
                                       text="<", font="Verdana 10", command=self.prev_track)

        self.Pause_resume_button = Button(self.Control_buttons_frame, bg="#000000", fg="#ffffff", activebackground="#000000",
                                     bd=7,
                                     width=6, height=1, font="Verdana 10",
                                     text="play", command=self.play)

        # Sliders

        self.Music_Slider = Scale(self.Main_bottom_frame, state=DISABLED, orient="horizontal",
                             troughcolor="#ffffff", bg="#000000", resolution=1, repeatdelay=1, showvalue=False,
                             length=330, from_=0, activebackground="#000000", command=self.slideOfmusicSlider)
        self.Music_Slider.bind('<ButtonRelease-1>', self.manipulate_track_time)
        self.Music_Slider.bind('<ButtonPress-1>', self.stop_while_manipulating)

        self.Volume_Slider = Scale(self.Volume_Slider_frame, orient="horizontal", bg="#000000", troughcolor="#ffffff",
                              showvalue=False, activebackground="#000000",
                              length=80, from_=0, to=1, resolution=0.01, command=self.manipulate_volume)
        self.Volume_Slider.set(self.current_volume)
        self.Volume_Slider.pack(side=RIGHT)

        # Labels

        self.Track_length_hms_label = Label(self.Track_time_frame, bg="#ffffff", text="0:00:00")

        self.Time_passed_label = Label(self.Track_time_frame, bg="#ffffff", text="0:00:00")

        # Packing widgets into frames
        self.Select_track_button.pack(pady=10)

        # Playlist_scrollbar.pack(side=RIGHT,fill=Y)
        self.new_slider.pack(side=RIGHT, fill=Y)

        self.Track_box.pack(padx=20)
        self.Select_new_track_button.pack(fill=X, padx=20)

        self.Music_Slider.pack(side=TOP)

        self.Previous_track_button.pack(side=LEFT)
        self.Skip_backwards_button.pack(side=LEFT)
        self.Pause_resume_button.pack(side=LEFT)
        self.Skip_forward_button.pack(side=LEFT)
        self.Next_track_button.pack(side=LEFT)

        self.Time_passed_label.pack(side=LEFT)
        self.Track_length_hms_label.pack(side=RIGHT)

        self.master.mainloop()  # we need to use this method, in order to constantly keep our window ready


    def know_track_duration(self, path_to_track):
        try:
            print(path.dirname((path.abspath(__file__))))
            process = run(
                f'ffprobe -v quiet -show_entries format=duration -of default=noprint_wrappers=1 "{self.current_tracks_path + "/" + self.current_track_title}"',
                shell=True, capture_output=True, text=True, cwd=path.dirname((path.abspath(__file__))))
            duration = process.stdout.split("=")  # this is gonna be something like duration=370.00032
            duration = duration[-1]
            duration = int(float(duration))
            return duration
        except Exception as e:
            print(e)

    #  interface functions

    def select_tracks(self):
        try:
            selected_tracks = filedialog.askopenfilenames(initialdir="C:/", filetypes=self.media_filetypes)
            if not selected_tracks:
                return
            else:
                tracks_num = len(selected_tracks)
                if tracks_num > 10:
                    self.new_slider.config(to=tracks_num - 10, state=ACTIVE)
                self.Track_box.delete(0, END)
            self.current_tracks_path = (path.split(selected_tracks[0]))[0]
            for track_title in selected_tracks:
                track_title = (track_title.split('/'))[-1]
                self.Track_box.insert(END, track_title)
            mixer.init()
            self.Music_Slider.config(state=ACTIVE)

        except Exception as e:
            print(e)

    def play(self):
        self.is_playing = True
        self.Pause_resume_button.config(text="pause", command=self.pause)
        try:
            mixer.music.play(start=self.Music_Slider.get())
            self.update_Music_Slider_position()
        except Exception as e:
            print(e)

    def replay(self):
        self.Pause_resume_button.config(text="replay", command=self.pause)
        self.Music_Slider.set(0)
        self.play()

    def pause(self):
        self.is_playing = False
        self.Pause_resume_button.config(text="play", command=self.play)
        try:
            self.Time_passed_label.after_cancel(self.after_id)
            mixer.music.stop()
        except Exception as e:
            print(e)


    def play_selected_track(self):
        mixer.music.stop()
        mixer.music.unload()
        try:
            self.Time_passed_label.after_cancel(self.after_id)
        except Exception as e:
            print(e)
        self.current_track_title = self.Track_box.get(ACTIVE)
        self.track_duration = self.know_track_duration(self.current_tracks_path)
        self.Track_length_hms_label.config(text=timedelta(seconds=self.track_duration))
        self.Music_Slider.config(to=self.track_duration)
        self.Music_Slider.set(0)
        self.Time_passed_label.config(text="0:00:00")
        self.Track_being_played.config(text=self.current_track_title)
        self.Track_being_played.pack(side=BOTTOM, pady=3)
        mixer.music.load(self.current_tracks_path + "/" + self.current_track_title)
        self.play()

    def skip_forward(self):
        if self.is_playing:
            self.is_playing = False
            self.Time_passed_label.after_cancel(self.after_id)
            current_pos = self.Music_Slider.get()
            mixer.music.stop()
            self.Music_Slider.set(current_pos + 4)
            self.play()
        else:
            current_pos = self.Music_Slider.get()
            self.Music_Slider.set(current_pos + 5)

    def skip_backwards(self):
        if self.is_playing:
            self.is_playing = False
            self.Time_passed_label.after_cancel(self.after_id)
            current_pos = self.Music_Slider.get()
            mixer.music.stop()
            if current_pos <= 5:
                self.Music_Slider.set(0)
            else:
                self.Music_Slider.set(current_pos - 6)
            self.play()
        else:
            current_pos = self.Music_Slider.get()
            if current_pos <= 5:
                self.Music_Slider.set(0)
            else:
                self.Music_Slider.set(current_pos - 5)

    def next_track(self):
        index = self.Track_box.get(0, "end").index(self.current_track_title)
        self.Track_box.selection_clear(0, "end")

        if self.Track_box.size() == index + 1:
            self.Track_box.activate(0)
            self.Track_box.selection_set(0)
            self.play_selected_track()
            return

        self.Track_box.activate(index + 1)
        self.Track_box.selection_set(index + 1)
        self.play_selected_track()

    def prev_track(self):
        index = self.Track_box.get(0, "end").index(self.current_track_title)
        self.Track_box.selection_clear(0, "end")

        if index == 0:
            self.Track_box.activate(self.Track_box.size() - 1)
            self.Track_box.selection_set(self.Track_box.size() - 1)
            self.play_selected_track()
            return

        self.Track_box.activate(index - 1)
        self.Track_box.selection_set(index - 1)
        self.play_selected_track()

    def update_Music_Slider_position(self):
        current_song_position = self.Music_Slider.get()
        if self.is_playing:
            self.after_id = self.Time_passed_label.after(1000, self.update_Music_Slider_position)
            self.Music_Slider.set(current_song_position + 1)

    def manipulate_volume(self, x): # баг тут
        try:
            if self.is_playing:
                mixer.music.set_volume(self.Volume_Slider.get())
            else:
                pass
        except Exception as e:
            print(e)

    def manipulate_track_time(self, curr_time):
        if self.autoplay & (self.Music_Slider.get() == self.track_duration):

            index = self.Track_box.get(0, "end").index(self.current_track_title)
            self.Track_box.selection_clear(0, "end")
            if self.Track_box.size() != index + 1:
                self.Track_box.activate(index + 1)
                self.Track_box.selection_set(index + 1)
                self.play_selected_track()
                return
            else:
                self.Track_box.activate(0)
                self.Track_box.selection_set(0)
                self.play_selected_track()
                return
        elif self.Music_Slider.get() == self.track_duration:
            self.Pause_resume_button.config(text="replay", command=self.replay)
            self.Time_passed_label.after_cancel(self.after_id)
            self.is_playing = False
        if self.is_playing:
            self.play()

    def stop_while_manipulating(self, x):
        if self.is_playing:
            self.Time_passed_label.after_cancel(self.after_id)
            mixer.music.stop()

    def slideOfmusicSlider(self, x):
        self.Time_passed_label.config(text=timedelta(seconds=int(x)))
        if self.autoplay & (int(x) == self.track_duration):

            index = self.Track_box.get(0, "end").index(self.current_track_title)
            self.Track_box.selection_clear(0, "end")
            if self.Track_box.size() != index + 1:
                self.Track_box.activate(index + 1)
                self.Track_box.selection_set(index + 1)
                self.play_selected_track()
                return
            else:
                self.Track_box.activate(0)
                self.Track_box.selection_set(0)
                self.play_selected_track()
                return
        elif int(x) == self.track_duration:
            self.Pause_resume_button.config(text="replay", command=self.replay)
            self.Time_passed_label.after_cancel(self.after_id)
            self.is_playing = False

    def scrollbar_mouse_control(self):
        self.Playlist_scrollbar.set()

    def enable_autoplay(self):
        if self.autoplay:
            self.autoplay = False
        else:
            self.autoplay = True




#  utility functions

App = MusicPlayer()



