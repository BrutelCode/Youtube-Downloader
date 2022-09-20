import requests
import threading
from time import sleep
from pafy import new
from os import path, remove
from RightClicker import RightClicker
from requests.exceptions import MissingSchema
from moviepy.video.io.VideoFileClip import VideoFileClip
from EmptyFieldException import EmptyFieldException, NotSelectedFolder
from tkinter import Entry, Button, Tk, Canvas, Label, filedialog, IntVar, messagebox

# Initialize Tkinter GUI
root = Tk(className=" Youtube Downloader")
root.resizable(False, False)
root.eval('tk::PlaceWindow . center')
root.iconbitmap('Youtube_ico.ico')

# Use the tkinter GUI
canvas1 = Canvas(root, width=400, height=150, relief='raised')
canvas1.pack()

label2 = Label(root, text='Youtube URL:')
label2.config(font=('helvetica', 15))
canvas1.create_window(200, 30, window=label2)

entry1 = Entry(root)
entry1.pack()
entry1.bind("<Button-3>", RightClicker)
canvas1.create_window(195, 60, window=entry1, width=235)

# Global variable that triggered when downloading a video
downloading_var = IntVar(0)

# Function to downloading the video in best quality
def DownloadVideo():
    try:
        # Get the input
        x1 = entry1.get()

        # Check if is it empty
        if x1 == "" or x1.isspace():
            raise EmptyFieldException()

        # Check if it is valid(Youtube URL) with HTTP REQUEST
        valid = requests.get(x1)

        # Check if is it valid(Youtube URL) with REGEX
        # valid = search(RegexUrl, x1)

        if valid.status_code == 200:
            label3 = Label(root, bg="green", text="Starting Download...", font=('helvetica', 10), width=28)
            canvas1.create_window(200, 140, window=label3)
            root.update()

            # URL
            video = new(x1)

            # Get the title of video
            title = video.title

            # Get all available streams
            # streams = video.streams
            #  for i in streams:
            #      print(i)

            # Best quality of video
            best = video.getbest()
            print(best.resolution, best.extension)

            # Choose the directory to download and keeping the path
            folder_selected = filedialog.asksaveasfilename(filetypes=[('.mp4','*.mp4')], defaultextension=".mp4")

            if folder_selected == "":
                raise NotSelectedFolder()

            # Before we start to download a video we trigger a value that used in function download_video()
            downloading_var.set(1)

            # Download the video in selected folder
            best.download(folder_selected, progress = "MB", quiet=False)

            # Check if the file .mp4 exist after downloading
            if path.exists(folder_selected):
                label3.configure(text="The Downloading is Finish!", font=('helvetica',10,'bold'))
                root.update()
            else:
                label3.configure(text="The File doesn't exist.Try again!", bg="red")
                root.update()
        else:
            raise MissingSchema
    except (EmptyFieldException, NotSelectedFolder) as err:
        expect1 = Label(root, bg="red", text=err, font=('helvetica', 10), width=28)
        canvas1.create_window(200, 140, window=expect1)
    except MissingSchema:
        label4 = Label(root, bg="red", text=" Wrong URL. Type a valid URL! ", font=('helvetica', 10), width=28)
        canvas1.create_window(200, 140, window=label4)
    except BaseException:
        expect1 = Label(root, bg="red", text="Something went Wrong.Try Again!", font=('helvetica', 10), width=28)
        canvas1.create_window(200, 140, window=expect1)

# Function to downloading Mp4 Video and converting into Mp3 audio
def DownloadMp3():
    try:
        # Get the input
        x1 = entry1.get()

        # Check if is it empty
        if x1 == "" or x1.isspace():
            raise EmptyFieldException()

        # Check if is it valid(Youtube URL) with HTTP REQUEST
        valid = requests.get(x1)

        if valid.status_code == 200:
            label3 = Label(root, bg="green", text="Starting Download...", font=('helvetica', 10), width=28)
            canvas1.create_window(200, 140, window=label3)
            root.update()

            # URL
            video = new(x1)

            # Get the title of video
            title = video.title

            # Get all available streams
            # streams = video.streams
            #  for i in streams:
            #      print(i)

            # Best Quality of video
            best = video.getbest()

            # Choose the directory to downloading and keep the path
            folder_selected_mp4 = filedialog.asksaveasfilename(filetypes=[('.mp4','*.mp4')], defaultextension=".mp4")
            folder_selected_mp3 = str(folder_selected_mp4)
            folder_selected_mp3 = folder_selected_mp3.replace(folder_selected_mp3[-1], '3')

            if folder_selected_mp4 == "" or folder_selected_mp3 == "":
                raise NotSelectedFolder()

            # Before we start to download a video we trigger a value that used in function download_mp3()
            downloading_var.set(1)

            # Downloading the Video
            best.download(folder_selected_mp4)

            # Convert the existing .mp4 file into .mp3 file
            label3.configure(text="Converting the .mp4 to .mp3!")
            root.update()

            # Before we start to converting a video we trigger a value that used in function download_mp3()
            downloading_var.set(2)
            video = VideoFileClip(path.join(folder_selected_mp4))
            video.audio.write_audiofile(path.join(folder_selected_mp3))

            # Check if the .mp3 file exist after downloading
            if path.exists(folder_selected_mp3):

                # Close video
                video.close()

                # We have to delete the file because it didn't exist before
                if path.exists(folder_selected_mp4):
                    remove(folder_selected_mp4)

                label3.configure(text="The Converting is Finish!", font=('helvetica',10,'bold'))
                root.update()

            else:
                label3.configure(text="The .mp3 File doesn't exist.Try again!", bg="red")
                root.update()
        else:
            raise MissingSchema

    except (EmptyFieldException, NotSelectedFolder) as err:
        expect1 = Label(root, bg="red", text=err, font=('helvetica', 10), width=28)
        canvas1.create_window(200, 140, window=expect1)
    except MissingSchema:
        label4 = Label(root, bg="red", text=" Wrong URL. Type a valid URL! ", font=('helvetica', 10), width=28)
        canvas1.create_window(200, 140, window=label4)
    except BaseException:
        expect1 = Label(root, bg="red", text="Something went Wrong.Try Again!", font=('helvetica', 10), width=28)
        canvas1.create_window(200, 140, window=expect1)


def main():

    root.update()

    # Function that opens a thread to refresh the main window when downloading a video
    def download_video():
        button2.config(command="")
        label_downloading = Label()
        counter = 0
        x = threading.Thread(target=DownloadVideo)
        x.start()
        while x.is_alive():
            root.update()
            if downloading_var.get() == 1:
                button1.config(command="")
                if counter == 0:
                    label_downloading = Label(root, bg="green",text="Downloading.", font=('helvetica', 10), width=28)
                    canvas1.create_window(200, 140, window=label_downloading)
                    button1.config(command="")
                    root.update()

                for i in range(1,4):
                    sleep(1)
                    label_downloading.config(text="Downloading"+"."*i)
                    root.update()

                counter +=1
        else:
            if label_downloading.winfo_exists():
                label_downloading.destroy()
            downloading_var.set(0)
            button1.config(command=download_video)
            button2.config(command=download_mp3)


    # Function that opens a thread to refresh the main window when downloading an .mp4 video and converting it to .mp3 file
    def download_mp3():
        button1.config(command="")
        label_downloading = Label()
        label_converting = Label()
        counter1 = 0
        counter2 = 0
        x = threading.Thread(target=DownloadMp3)
        x.start()
        while x.is_alive():
            root.update()
            if downloading_var.get() == 1:
                button2.config(command="")
                if counter1 == 0:
                    label_downloading = Label(root, bg="green",text="Downloading.", font=('helvetica', 10), width=28)
                    canvas1.create_window(200, 140, window=label_downloading)
                    button2.config(command="")
                    root.update()

                for i in range(1,4):
                    sleep(1)
                    label_downloading.config(text="Downloading"+"."*i)
                    root.update()

                counter1 +=1
            elif downloading_var.get() == 2:
                button2.config(command="")
                if counter2 == 0:
                    label_converting = Label(root, bg="green", text="Converting to mp3.", font=('helvetica', 10), width=28)
                    canvas1.create_window(200, 140, window=label_converting)
                    button2.config(command="")
                    root.update()

                for i in range(1, 4):
                    sleep(1)
                    label_converting.config(text="Converting to mp3" + "." * i)
                    root.update()

                counter2 += 1
        else:
            if label_downloading.winfo_exists():
                label_downloading.destroy()
            if label_converting.winfo_exists():
                label_converting.destroy()
            downloading_var.set(0)
            button2.config(command=download_mp3)
            button1.config(command=download_video)


    button1 = Button(text='Download Video', command=download_video, bg='brown', fg='white',
                     font=('helvetica', 9, 'bold'))
    canvas1.create_window(130, 100, window=button1)


    button2 = Button(text='Download MP3', command=download_mp3, bg='brown', fg='white',
                     font=('helvetica', 9, 'bold'))
    canvas1.create_window(265, 100, window=button2)

    # When the user is going to close the window an extra box is appear
    def on_closing():
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            root.destroy()

    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()

main()
