import os, base64, atexit, platform, ctypes

from tkinter import *
from tkinter import messagebox
from os.path import expanduser
root = Tk()
root.title('Access denied')
root.geometry('500x500')
root.attributes('-topmost', True)
root.attributes('-fullscreen', True)
root.wait_visibility(root)
root.attributes('-alpha', 0.85)
root.configure(bg='black')

FILENAME = expanduser('~') + '/.data'

def inverseCase(text):
    output = ''
    for char in text:
        if char.islower():
            output += char.upper()
        else:
            output += char.lower()
    return output

def encode2Base64(text):
    stringBytes = text.encode('ascii')
    base64Bytes = base64.b64encode(stringBytes)
    output = base64Bytes.decode('ascii')
    return output

def decodeBase64(cipher):
    base64Bytes = cipher.encode('ascii')
    stringBytes = base64.b64decode(base64Bytes)
    output = stringBytes.decode('ascii')
    return output

def salvador(text):
    text = encode2Base64(text)
    text = text[::-1]
    text = encode2Base64(text)
    text = inverseCase(text)
    return text

def openFolder():
    passw = field.get()
    current = os.getcwd().replace('\\', '/') + '/' + __file__
    hiddenf = os.getcwd().replace('\\', '/') + '/.' + __file__[0:__file__.rindex('.')]
    if platform.system() == 'Windows':
        current = __file__.replace('\\', '/')
        hiddenf = __file__[0:__file__.rindex('.')].replace('\\', '/')
    current = current[0:current.rindex('.')]
    secretK = 'empty'
    stored = list()
    with open(FILENAME, 'r') as data:
        stored = data.read().split()    
    for st in stored:
        if salvador(current) == st[0:st.rindex('|')]:
            secretK = st[st.rindex('|')+1:]
            stored.remove(st)
            break
    if salvador(passw) == secretK:
        os.remove(FILENAME)
        with open(FILENAME, 'a') as data:
            for st in stored:
                data.write(st + '\n')
        if platform.system() == 'Linux':
            os.rename(hiddenf, current)
            os.system('xdg-open "%s"' % current)
        else:
            ctypes.windll.kernel32.SetFileAttributesW(current, 0x80)
            os.system('explorer "%s"' % current[current.rindex('/')+1:])
        exit(atexit.register(lambda file = __file__: os.remove(file)))
    else:
        messagebox.showerror("Error", "Incorrect password")
        field.delete(0, "end")


def close():
    root.destroy()

frame = Frame(root, pady=20, padx=20, bd=5, relief=RAISED)
frame.place(anchor=CENTER, relx=.5, rely=.45)
title   = Label(frame, text = 'This folder is protected!', font = ('Ubuntu', 14))
caption = Label(frame, text = 'Enter password:', font = ('Ubuntu', 18))
field   = Entry(frame, relief = FLAT, borderwidth = 5, width = 30, justify=CENTER, show='●', font=('Ubuntu', 22))
submit  = Button(frame, text = 'Open', height=2, width=15, font=('Ubuntu', 16), command=openFolder)
leave   = Button(frame, text = 'IDK', height=2, width=15, font=('Ubuntu', 16), command=close)

# title.place(anchor=CENTER, relx=.5, rely=.3)
# caption.place(anchor=CENTER, relx=.5, rely=.35)
# field.place(anchor=CENTER, relx=.5, rely=.40)
# submit.place(anchor=CENTER, relx=.5, rely=.47)
# leave.place(anchor=CENTER, relx=.5, rely=.55)

title.pack(pady=20)
caption.pack(pady=5)
field.pack()
submit.pack(pady=10)
leave.pack()

root.mainloop()
