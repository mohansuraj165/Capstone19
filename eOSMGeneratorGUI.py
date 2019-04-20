from tkinter import *
from tkinter import filedialog
import Start as S

'''
Handles folder browse click
'''
def FileDialog():
    path = filedialog.askdirectory(initialdir="/")
    entPath.config(state='normal')
    entPath.delete(0,END)
    entPath.insert(0,path)
    entPath.config(state='readonly')

'''
Handles start button click
'''
def Start():
    path = entPath.get()
    if path=="":
        return
    S.Main(path)


#Creating new window
root=Tk()
root.title("EOSM-Generator")
root.geometry("500x400")

app=Frame(root)
app.grid()

lblSelectFolder = Label(app, text="Select a folder")
lblSelectFolder.grid(column=0, row=1, padx=20, pady=20)

btnBrowse = Button(app, text="Browse",command=FileDialog)
btnBrowse.grid(column=0, row=3)

entPath = Entry(app, state='readonly', width=50)
entPath.grid(column=1,row=3)

btnStart = Button(app,text="Start", command=Start)
btnStart.grid(column=0,row=5, padx=20, pady=20)

root.mainloop()


