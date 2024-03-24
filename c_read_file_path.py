import tkinter as tk
from tkinter import ttk
from tkinter import filedialog

def Read_file_path():
    Read_file_path(tk.Tk)

import os

class Read_file_path(tk.Toplevel):
    alive =False

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry("600x400+210+210")
        self.title('Open file path')
        self.focus_set()
        self.__class__.alive =True

        #no need to access
        tk.Label(self, text="any message here").pack()

        self.entry1 = tk.Entry(self, width=60)
        self.entry1.pack()

        self.button1 = tk.Button(self, text="select path", command=self.read_file_path)
        self.button1.pack()

        self.text1 = tk.Text(self)
        self.text1.pack(expand=True, fill='x')

        self.scroll = tk.Scrollbar(self)
        self.scroll.config(command=self.text1.yview)
        self.text1.config(yscrollcommand=self.scroll.set)
        self.scroll.pack(side=tk.RIGHT, fill=tk.Y)

    def read_file_path(self):
        self.dir_path = filedialog.askdirectory()
        #why losing focus after above?
        self.focus_set()
        self.entry1.delete(0,tk.END)
        self.entry1.insert(0, self.dir_path)
        print(self.dir_path)

        self.text1.delete("1.0", tk.END)

        for root, dir, files in os.walk(self.dir_path):
            for file in files:
                self.text1.insert(tk.END, "\n"+os.path.join(root, file))

        self.text1.pack(expand=True, fill='both')

    def destroy(self):
        self.__class__.alive =False
        return super().destroy()

# self testable
if __name__=="__main__" :
    app= Read_file_path()
    app.mainloop()