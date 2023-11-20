import customtkinter as ctk
from customtkinter import (
    CTkScrollableFrame,
    CTkEntry,
    CTkButton,
    CTkComboBox)
from api.search import yt_search, parallel_task
from app_gui.videobutton import VideoButton
from app_gui.frame import (
    Frame,
    InfoFrame,
    VideoFrame,
    PlaylistWindow, )

ctk.set_default_color_theme("dark-blue")
ctk.set_appearance_mode('dark')


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title('youtube downloader')
        self.iconbitmap('C:\PyProjects\learning_youtube_api\icon.ico')
        self.geometry('900x550')
        self.grid_columnconfigure((0, 1), weight=1)

        # ------------------------> class variables
        self.type_var = ctk.IntVar(value=0)
        self.id_var = ctk.StringVar(value='')
        self.result_count = ctk.StringVar(value='')
        # ------------------------>

        self.search_frame = Frame(self, row=0, column=0, fg_color='transparent',
                                  columnspan=2, width=600)

        self.control_frame = Frame(self, row=1, column=0, fg_color='transparent',
                                   minsize=100)
        self.info_frame = InfoFrame(self, row=1, column=1)

        self.entry = CTkEntry(self.search_frame, placeholder_text='python',
                              width=500)
        self.entry.grid(row=0, column=0, padx=20, pady=(10, 0))

        # ------------------------> Control Buttons section
        self.buttons_frame = Frame(self.search_frame, row=1, column=0,
                                   fg_color='transparent')
        self.buttons_frame.grid_columnconfigure(0, weight=1)

        self.search_button = CTkButton(self.buttons_frame,
                                       text='search',
                                       state='disabled',
                                       command=self.search_results)
        self.search_button.grid(row=1, column=0, pady=10, padx=(30, 70))

        # ------------------------>
        self.result_values = [str(x) for x in range(5, 30, 5)]
        self.textbox = CTkComboBox(self.buttons_frame,
                                   variable=self.result_count,
                                   values=self.result_values)
        self.textbox.grid(row=1, column=1, pady=10, padx=(30, 70))
        # ------------------------> Radio Buttons section
        self.radio_frame = Frame(self.search_frame, row=2, column=0,
                                 fg_color='transparent', height=100, width=500)

        self.radio_buttons = []
        for idx, text in enumerate(('video', 'playlist')):
            b = ctk.CTkRadioButton(self.radio_frame,
                                   text=text, variable=self.type_var,
                                   value=idx, width=250)
            b.grid(row=0, column=idx)
            b.columnconfigure(0, weight=1)
            self.radio_buttons.append(b)
        # ------------------------>

        self.scroll_frame = CTkScrollableFrame(self.search_frame, width=500, height=200)
        self.scroll_frame.grid(row=3, column=0)

        # binding
        self.entry.bind("<KeyRelease>", self.is_entry_empty)

    def search_results(self):
        """
        Display found videos on Scrollable Frame via CTkButton
        """
        # clear the id_var
        self.id_var.set(value='')
        self.control_frame.destroy()

        yt_type = self.type_var.get()  # type (video, playlist, channel)
        if yt_type == 0:  # video
            self.control_frame = VideoFrame(master=self, row=1,
                                            info_frame=self.info_frame,
                                            column=0, width=250)
        elif yt_type == 1:  # playlist
            self.control_frame = PlaylistWindow(master=self, row=1,
                                                info_frame=self.info_frame,
                                                textbox=self.info_frame.textbox,
                                                fg_color='transparent',
                                                column=0, width=250)
        self.control_frame.textbox = self.info_frame.textbox

        # function  that is responsible for the frame's actions during search
        self.control_frame.search()

        # clear the scrollable frame
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()

        # display found results on ScrollFrame
        limit = int(self.result_count.get())
        parallel_task(self, yt_search, max_results=limit)

    def is_entry_empty(self, *args):
        """
        Checks if an input field is empty
        """
        # Getting the content of ctkEntry
        entry_content = self.entry.get()

        # If the field is empty, deactivate the button, otherwise activate it
        if not entry_content:
            self.search_button.configure(state="disabled")
        else:
            self.search_button.configure(state="normal")

    def select_button(self, widget: VideoButton):
        """
        highlights the user-selected button
        :param widget: selected button
        """
        if not widget.pressed:  # check if button has not been pressed

            for w in self.scroll_frame.winfo_children():
                if isinstance(w, VideoButton):  # if widget is VideoButton
                    if widget == w:
                        self.control_frame.selected(widget=widget)
                        w.change_state(True)
                        self.id_var.set(value=w.yt_id)
                    else:
                        w.change_state(False)


if __name__ == "__main__":
    app = App()
    app.mainloop()
