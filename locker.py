#/usr/bin/python3.9

import base64, ctypes, platform

from shutil import copy
from os import remove, rename, path
from tkinter import *
from tkinter import filedialog

FILENAME = path.expanduser('~') + '/.data'

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

def onselect(e):
    if len(e.widget.curselection()) == 0:
        btn3['state'] = DISABLED
    else:
        btn3['state'] = NORMAL

def salvador(text, cmd):
    if cmd == 1:
        text = encode2Base64(text)
        text = text[::-1]
        text = encode2Base64(text)
        text = inverseCase(text)
    elif cmd == 0:
        text = inverseCase(text)
        text = decodeBase64(text)
        text = text[::-1]
        text = decodeBase64(text)
    return text

def chooseDirectory():
    global path2folder
    path2folder = filedialog.askdirectory()
    field.delete(0, "end")
    field.insert(0, path2folder[path2folder.rindex('/') + 1:])
    btn2.configure(state=NORMAL)

def lock():
    global path2folder
    passw = passwf.get()
    if path2folder not in lockedFolders.get(0, "end"):
        with open(FILENAME, 'a') as d:
            d.write(salvador(path2folder, 1) + '|' + salvador(passw, 1) + '\n')  
        lockedFolders.insert(1, path2folder)
    field.delete(0, 'end')
    passwf.delete(0, 'end')
    if platform.system() == 'Linux':
        rename(path2folder, path2folder[0:path2folder.rindex('/')+1] + '.' + path2folder[path2folder.rindex('/') + 1:])
        copy('.locked.py', path2folder[0:path2folder.rindex('/')+1] + path2folder[path2folder.rindex('/') + 1:] + '.py')
    else:
        ctypes.windll.kernel32.SetFileAttributesW(path2folder, 0x02)
        copy('.locked.py', path2folder[0:path2folder.rindex('/')+1] + path2folder[path2folder.rindex('/') + 1:] + '.pyw')
    path2folder = ''
    btn2.configure(state=DISABLED)

def unlock():
    collection = lockedFolders.curselection()
    stored   = []
    selected = []

    for se in collection:
        currentPath = lockedFolders.get(se)
        selected.append(currentPath)
        if platform.system() == 'Linux':
            remove(currentPath + '.py')
            rename(currentPath[0:currentPath.rindex('/')+1] + '.' + currentPath[currentPath.rindex('/')+1:], currentPath)
        else:
            remove(currentPath + '.pyw')
            ctypes.windll.kernel32.SetFileAttributesW(currentPath, 0x80)
    
    with open(FILENAME, 'r') as d:
        stored = d.read().split()
    
    remove(FILENAME)

    with open(FILENAME, 'a') as d:
        for s in stored:
            cur = salvador(s[0:s.rindex('|')], 0)
            if cur not in selected:
                d.write(s + '\n')

    for idx in collection:
        lockedFolders.delete(idx)

window = Tk()

window.title('DirLocker')   
window.geometry('500x530')
window.resizable(height=False, width=False)

title = Label(text = 'Welcome to DirLocker!', font = ('Ubuntu', 14))
title.place(anchor = CENTER, relx = .5, rely = .07)

description = Label(text = 'DirLocker - System utility created by meirbnb for, which enables\nlocking directories using different passwords.', justify=LEFT, font=('Roboto', 10))
description.place(anchor = CENTER, relx = .5, rely = .17)

hint = Label(text = 'Locked folder(s): ', font = ('Ubuntu', 12))
hint.place(relx = .055, rely = .23)
lockedFolders = Listbox(font=('Ubuntu', 12), width=44, selectmode=MULTIPLE, yscrollcommand=True)
lockedFolders.place(anchor = CENTER, relx = .5, rely = .48)
lockedFolders.bind('<<ListboxSelect>>', onselect)

fint = Label(text = 'Folder: ', font = ('Ubuntu', 12))
field = Entry(font = ('Ubuntu', 12), relief=FLAT, borderwidth=5, width=31)
field.bind("<Key>", lambda a: "break")
btn = Button(text = '...', font = ('Ubuntu', 12), command = chooseDirectory)
fint.place(anchor = CENTER, relx = .116, rely = .73)
field.place(anchor = CENTER, relx = .56, rely = .73)
btn.place(anchor = CENTER, relx = .91, rely = .73)

passwh = Label(text = 'Password: ', font = ('Ubuntu', 12))
passwf = Entry(font = ('Ubuntu', 12), relief=FLAT, borderwidth=5, show='●', width=34)
passwh.place(anchor = CENTER, relx = .14, rely = .812)
passwf.place(anchor = CENTER, relx = .59, rely = .81)

btn2 = Button(text = 'Lock', font = ('Ubuntu', 12), command = lock, width=19, height=2, state=DISABLED)
btn2.place(anchor = CENTER, relx = .27, rely = .915)

btn3 = Button(text = 'Unlock', font = ('Ubuntu', 12), command = unlock, width=19, height=2, state=DISABLED)
btn3.place(anchor = CENTER, relx = .73, rely = .915)

try:
    with open(FILENAME, 'r') as d:
        for folder in d.read().split():
            folder = salvador(folder[0:folder.index('|')], 0)
            lockedFolders.insert(1, folder)
except:
    pass
window.mainloop()
