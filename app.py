import tkinter as tk
import os
from tkinter.filedialog import askdirectory
from pytube import YouTube
from moviepy.video.io.VideoFileClip import VideoFileClip
from threading import Thread

CANVAS_HEIGHT = 400
CANVAS_WIDTH = 500
file_size = 0


def convert_to_audio(file_path):
    button['text'] = 'Conversion en mp3...'
    button['state'] = tk.DISABLED
    yt_url_entry['state'] = tk.DISABLED

    try:
        base, ext = os.path.splitext(file_path)
        video = VideoFileClip(file_path)
        video.audio.write_audiofile(base + '.mp3')
        video.close()
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
        st = yt.streams.first()

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
root.geometry('500x300')

canvas = tk.Canvas(root, bg='#DBDBDB')
canvas.pack()

frame = tk.Frame(root, bg='#B0B5B3')
frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER, relwidth=0.9, relheight=0.9)

error = tk.Label(frame, text='Une erreur est survenue, veuillez recommencer.', fg='red')
success = tk.Label(frame, text='Vidéo téléchargée avec succès!', fg='green')

yt_url_entry_label = tk.Label(frame, text='YouTube video URL:')
yt_url_entry_label.pack(side='top', pady=(10, 0))

yt_url_entry = tk.Entry(frame, width=25)
yt_url_entry.pack(side='top', pady=10)

chosen_path_entry_label = tk.Label(frame, text='Destination:')
chosen_path_entry_label.pack(side='top', pady=(10, 0))

chosen_path_frame = tk.Frame(frame, bg='#B0B5B3')
chosen_path_frame.pack(side='top')

chosen_path_entry = tk.Entry(chosen_path_frame, width=15, state=tk.DISABLED)
chosen_path_entry.pack(side='left', pady=10)

chosen_path_button = tk.Button(chosen_path_frame, text='Parcourir...', command=dest_path_callback)
chosen_path_button.pack(side='right', padx=(5, 0))

progress_label = tk.Label(frame)

button = tk.Button(frame, text='Submit', command=submit_callback)
button.pack(side='bottom', pady=(0, 10))

root.mainloop()
