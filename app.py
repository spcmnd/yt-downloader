import tkinter as tk
import os
from tkinter.filedialog import askdirectory
from pytube import YouTube
from moviepy.audio.io.AudioFileClip import AudioFileClip
from threading import Thread
from PIL import Image, ImageTk


# Global variables
background_color = '#fff'
file_size = 0
small_font = ('Calibri', 10)
global_font = ('Calibri', 12)
global_font_bold = ('Calibri', 12, 'bold')
version_number = 'v' + str(open('VERSION', 'r').read())


def convert_to_audio(file_path):
    button['text'] = 'Conversion en mp3...'
    button['state'] = tk.DISABLED
    yt_url_entry['state'] = tk.DISABLED

    try:
        base, ext = os.path.splitext(file_path)
        audio = AudioFileClip(file_path)
        audio.write_audiofile(base + '.mp3')
        audio.close()
        os.remove(file_path)
    except Exception as e:
        button_initial_state()
        display_error()
        print(e)
        raise

    yt_url_entry['state'] = tk.NORMAL
    yt_url_entry.delete(0, tk.END)
    button_initial_state()
    display_success()


def progress_download(stream=None, chunk=None, bytes_remaining=None):
    percent = (100 * ((file_size - bytes_remaining) / file_size))
    button['text'] = '{:00.0f}% téléchargé...'.format(percent)
    return


def complete_download(stream=None, chunk=None):
    button_initial_state()
    return


def dest_path_callback():
    path = str(askdirectory())
    chosen_path_entry['state'] = tk.NORMAL
    chosen_path_entry.delete(0, tk.END)
    chosen_path_entry.insert(0, path)
    chosen_path_entry['state'] = tk.DISABLED
    return


def submit_callback():
    hide_error()
    hide_success()
    url = str(yt_url_entry.get())
    thread = Thread(target=download_video, args=(url,))
    thread.start()


def download_video(url):
    button['state'] = tk.DISABLED

    try:
        yt = YouTube(url)
        st = yt.streams.filter(only_audio=True, file_extension='mp4').first()

        if yt.title == 'YouTube':
            # Restart to avoid wrong name
            submit_callback()
            return

        global file_size
        file_size = st.filesize
        download_path = chosen_path_entry.get()

        if len(download_path) == 0:
            download_path = 'downloads/'

        yt.register_on_complete_callback(complete_download)
        yt.register_on_progress_callback(progress_download)
        downloaded_yt = st.download(download_path)
    except Exception as e:
        button_initial_state()
        display_error()
        print(e)
        raise

    file_path = os.path.join(os.getcwd(), 'downloads', downloaded_yt)
    convert_to_audio(file_path)


def display_success():
    success.pack(side='top', pady=10)


def hide_success():
    success.pack_forget()


def display_error():
    error.pack(side='top', pady=10)


def hide_error():
    error.pack_forget()


def button_initial_state():
    button['state'] = tk.NORMAL
    button['text'] = 'Submit'


root = tk.Tk()
root.title('Youtube Downloader')
root.geometry('800x400')

canvas = tk.Canvas(root, bg=background_color)
canvas.place(relwidth=1, relheight=1)

frame = tk.Frame(root, bg=background_color)
frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER, relwidth=0.9, relheight=0.9)

error = tk.Label(frame, text='Une erreur est survenue, veuillez recommencer.', fg='red', bg='#fff', font=global_font_bold)
success = tk.Label(frame, text='Vidéo téléchargée avec succès!', fg='green', bg='#fff', font=global_font_bold)

im = Image.open('assets/youtube_icon.png').resize((115, 85))
youtube_logo = ImageTk.PhotoImage(im)
yt_logo_label = tk.Label(frame, image=youtube_logo, width=150, bg=background_color)
yt_logo_label.pack(side='top', pady=(10, 0))

yt_url_entry_label = tk.Label(frame, text='YouTube video URL:', bg=background_color, font=global_font_bold)
yt_url_entry_label.pack(side='top', pady=(10, 0))

yt_url_entry = tk.Entry(frame, font=global_font)
yt_url_entry.pack(side='top', pady=10, padx=10, fill=tk.X)

chosen_path_entry_label = tk.Label(frame, text='Destination:', bg=background_color, font=global_font_bold)
chosen_path_entry_label.pack(side='top', pady=(10, 0))

chosen_path_frame = tk.Frame(frame, bg=background_color)
chosen_path_frame.pack(side='top', fill=tk.X, padx=10)

chosen_path_entry = tk.Entry(chosen_path_frame, state=tk.DISABLED, font=global_font)
chosen_path_entry.pack(side='left', pady=10, fill=tk.X, expand=True)

chosen_path_button = tk.Button(chosen_path_frame, text='Parcourir...', command=dest_path_callback, font=global_font, fg='#fff', bg='#FF0000')
chosen_path_button.pack(side='right', padx=(5, 0))

button = tk.Button(frame, text='Submit', command=submit_callback, fg='#fff', bg='#FF0000', font=global_font)
button.pack(side='bottom', pady=(0, 10))

version_number_label = tk.Label(root, bg='#fff', font=small_font, text=version_number)
version_number_label.place(rely=1.0, relx=1.0, x=-10, y=-5, anchor=tk.SE)

root.mainloop()
