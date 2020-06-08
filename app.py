import tkinter as tk
from pytube import YouTube


def submit_callback():
    error.pack_forget()
    success.pack_forget()

    try:
        url = str(yt_url_entry.get())
        yt = YouTube(url)
        yt.streams.first().download('./downloads')
        error.pack_forget()
        success.pack(side='top', pady=10)
        yt_url_entry.delete(0, 'end')
    except:
        display_error()


def display_error():
    error.pack(side='top', pady=10)


root = tk.Tk()
root.title('Youtube Downloader')

canvas = tk.Canvas(root, width=300, height=200, bg='#DBDBDB')
canvas.pack()

frame = tk.Frame(root, bg='#B0B5B3')
frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER, relwidth=0.9, relheight=0.9)

error = tk.Label(frame, text='Une erreur est survenue, veuillez recommencer.', fg='red')
success = tk.Label(frame, text='Vidéo téléchargée avec succès!', fg='green')

yt_url_entry_label = tk.Label(frame, text="YouTube video URL:")
yt_url_entry_label.pack(side='top', pady=(10, 0))

yt_url_entry = tk.Entry(frame)
yt_url_entry.pack(side='top', pady=10)

button = tk.Button(frame, text='Submit', command=submit_callback)
button.pack(side='bottom', pady=(0, 10))

root.mainloop()
