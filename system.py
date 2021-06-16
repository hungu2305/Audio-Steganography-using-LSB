import tkinter
from tkinter import *
from tkinter import ttk, messagebox
from tkinter import filedialog
from PIL import ImageTk, Image
import wave
import os.path

root = Tk()
root.title('Audio Steganography')
root.geometry("1100x650")

tabControl = ttk.Notebook(root)
tab0 = Frame(tabControl)
tab1 = Frame(tabControl)
tabControl.add(tab0, text="ENCODE")
tabControl.add(tab1, text="DECODE")
tabControl.pack(expand=1, fill=BOTH)
#define tab0
bg = Image.open("bg.jpg")
resized_bg = bg.resize((1100,650), Image.ANTIALIAS)
bg0 = ImageTk.PhotoImage(resized_bg)
label0 = Label(tab0,image=bg0)
label0.pack(expand=True,fill=BOTH)
fileinput = Label(tab0, text="File Input", font=('times new roman', 25, 'bold'))
fileinput.place(x=10,y=30)
label1 = Label(tab0, text="Select the audio file to embedded !", fg='red')
label1.place(x=800,y=30)
label2 = Label(tab0, text="Enter the embedded text !", fg='red')
label2.place(x=400,y=250)
label3 = Label(tab0, text="Enter the name audio file to save after embedded !", fg='red')
label3.place(x=400,y=450)
label4 = Label(tab0, text='Select the folder to save file',fg='red')
label4.place(x=800,y=400)
button1 = Button(tab0,text="Browse input", bg='purple',fg='white',command=lambda :browseFiles())
button1.place(x=700,y=30)
button2 = Button(tab0,text="EMBEDDED",font=("times new roman", 15, 'bold'),bg='purple',fg='white', command=lambda :embedded())
button2.place(x=500,y=500)
button3 = Button(tab0,text="Browse output",bg='purple',fg='white', command=lambda :browsePath())
button3.place(x=700,y=400)
textinput = Label(tab0, text="Embedded text", font=("times new roman", 25, 'bold'))
textinput.place(x=10,y=200)
textinput_entry = Entry(tab0, font=("times new roman", 15, 'bold'))
textinput_entry.place(x=400,y=200,width=250)
fileoutput = Label(tab0, text="File Output", font=('times new roman', 25, 'bold'))
fileoutput.place(x=10,y=390)
fileoutput_entry = Entry(tab0,font=("times new roman", 15, 'bold'))
fileoutput_entry.place(x=400,y=390,width=250)
#define encode
def browsePath():
    root.pathname = filedialog.askdirectory(initialdir="/")
def browseFiles():
    root.filename = filedialog.askopenfilename(initialdir="/", title="Select a File", filetypes=(("Audio files", "*.wav*"), ("all files", "*.*")))
def embedded():
    print("\nEncoding Start....")
    if root.filename=="":
        messagebox.showerror("Error", "You need to choose the audio file")
    elif root.pathname=="":
        messagebox.showerror("Error", "You need to choose the folder to save file")
    elif textinput_entry.get()=="":
        messagebox.showerror("Error", "You need to enter the embedded text")
    elif fileoutput_entry.get()=="":
        messagebox.showerror("Error", "Audio file need a name to save!")
    else:
        audio = wave.open(root.filename, mode="rb")
        frame_bytes = bytearray(list(audio.readframes(audio.getnframes())))
        string = textinput_entry.get()
        print(string)
        string = string + int((len(frame_bytes) - (len(string) * 8 * 8)) / 8) * '#'
        bits = list(map(int, ''.join([bin(ord(i)).lstrip('0b').rjust(8, '0') for i in string])))
        for i, bit in enumerate(bits):
            frame_bytes[i] = (frame_bytes[i] & 254) | bit
        frame_modified = bytes(frame_bytes)
        for i in range(0, 10):
            print(frame_bytes[i])
        savename = os.path.join(root.pathname, fileoutput_entry.get() + ".wav")
        newAudio = wave.open(savename, 'wb')
        newAudio.setparams(audio.getparams())
        newAudio.writeframes(frame_modified)

        newAudio.close()
        audio.close()
        messagebox.showinfo("Success!", "The text has been successfully embedded")

#define tab1
label00 = Label(tab1,image=bg0)
label00.pack(expand=True,fill=BOTH)
fileinput1 = Label(tab1, text="File Input", font=('times new roman', 25, 'bold'))
fileinput1.place(x=10,y=30)
buttona = Button(tab1,text="Browse input", bg='purple',fg='white',command=lambda :browseFiles1())
buttona.place(x=700,y=30)
labela = Label(tab1, text="Select the audio file to decode !", fg='red')
labela.place(x=800,y=30)
buttonb = Button(tab1,text="EXTRACT", font=("times new roman", 15, 'bold'),bg='purple',fg='white', command=lambda :decode())
buttonb.place(x=500,y=200)
labelc = Label(tab1, text="Embedded Text:", font=('times new roman', 25, 'bold'))
labelc.place(x=10,y=300)
#define decode
def browseFiles1():
    root.filename1 = filedialog.askopenfilename(initialdir="/", title="Select a File",
                                               filetypes=(("Audio files", "*.wav*"), ("all files", "*.*")))
def decode():
    print("\nDecoding Starts..")
    if root.filename1 == "":
        messagebox.showerror("Error", "You need to select audio file!")
    else:
        audio = wave.open(root.filename1, mode='rb')
        frame_bytes = bytearray(list(audio.readframes(audio.getnframes())))
        extracted = [frame_bytes[i] & 1 for i in range(len(frame_bytes))]
        string = "".join(chr(int("".join(map(str, extracted[i:i + 8])), 2)) for i in range(0, len(extracted), 8))
        decoded = string.split("###")[0]
        T = Text(tab1, height=10, width=50)
        T.insert(tkinter.END, decoded)
        T.place(x=300, y=300)
        audio.close()
root.mainloop()