import tkinter as tk
from tkinter.filedialog import askdirectory
from pytube import YouTube
from moviepy.editor import *
from threading import Thread

CANVAS_HEIGHT = 400
CANVAS_WIDTH = 500
file_size = 0


def progress_download(stream=None, chunk=None, bytes_remaining=None):
    percent = (100 * ((file_size - bytes_remaining) / file_size))
    button['text'] = str(int(percent)) + '% téléchargé...'
    return


def dest_path_callback():
    path = str(askdirectory())
    chosen_path_entry.config(state=tk.NORMAL)
    chosen_path_entry.delete(0, tk.END)
    chosen_path_entry.insert(0, path)
    chosen_path_entry.config(state=tk.DISABLED)
    return


def submit_callback():
    hide_error()
    hide_success()
    url = str(yt_url_entry.get())
    thread = Thread(target=download_video, args=(url,))
    thread.start()


def download_video(url):
    try:
        yt = YouTube(url)

        if yt.title == 'YouTube.mp4':
            # Restart to avoid wrong name
            submit_callback()
            return

        global file_size
        file_size = yt.length
        download_path = chosen_path_entry.get()

        if len(download_path) == 0:
            download_path = 'downloads/'

        yt.register_on_progress_callback(progress_download)
        downloaded_yt = yt.streams.first().download(download_path)
    except Exception as e:
        display_error()
        print(e)
        raise

    yt_url_entry.delete(0, tk.END)
    file_path = os.path.join(os.getcwd(), 'downloads', downloaded_yt)
    base, ext = os.path.splitext(file_path)

    try:
        video = VideoFileClip(file_path)
        video.audio.write_audiofile(base + '.mp3')
    except Exception as e:
        display_error()
        print(e)
        raise

    os.remove(file_path)
    display_success()


def display_success():
    success.pack(side='top', pady=10)


def hide_success():
    success.pack_forget()


def display_error():
    error.pack(side='top', pady=10)


def hide_error():
    error.pack_forget()


root = tk.Tk()
root.title('Youtube Downloader')

canvas = tk.Canvas(root, width=CANVAS_WIDTH, height=CANVAS_HEIGHT, bg='#DBDBDB')
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
