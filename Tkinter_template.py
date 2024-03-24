import tkinter as tk
from tkinter import messagebox

from c_read_file_path import Read_file_path
import read_file_path

class MainWindow(tk.Tk):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry("600x400+200+200")
        self.title("Main Window")

        #create menu bar
        self.menubar = tk.Menu(self)

        #Create file menu
        self.filemenu = tk.Menu(self.menubar, tearoff=0)
        self.filemenu.add_command(label='new', command=self.file_new)
        self.filemenu.add_command(label='Read File Path', command=self.open_read_file_path)
        self.filemenu.add_command(label='Exit', command=self.quit)

        #bottome up.
        self.menubar.add_cascade(label="File", menu=self.filemenu)

        #Add help menu to show going left
        self.helpmenu =tk.Menu(self.menubar, tearoff=0)
        self.helpmenu.add_command(label = 'About', command=self.open_about)
        self.menubar.add_cascade(label="Help", menu=self.helpmenu)


        #set the menuba
        self.config(menu=self.menubar)

    # command should be in class
    def file_new (self):
        messagebox.showinfo("File new", "Yet you clicked file -> new menu" )
        # this shows in command
        print ("File new", "Yet you clicked file -> new menu" )

    def open_read_file_path(self):
        if Read_file_path.alive :
            self.read_file_path.focus_set()
        else:
            self.read_file_path = Read_file_path()

    def open_about (self):
        messagebox.showinfo("About", "Billy wanted help you" )
        # this shows in command
        print ("About", "Billy wanted help you" )

if __name__ == "__main__":
    main_window = MainWindow()
    main_window.mainloop()
