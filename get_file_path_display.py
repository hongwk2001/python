import tkinter as tk
import os
from tkinter import filedialog

class App(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry("600x400+200+200")
        self.title("File Path Display")

        tk.Label(self, text="test").pack()
        # Create a button to open the file selection dialog
        self.button = tk.Button(self, text="Select File", command=self.select_file)
        self.button.pack()

        # Create a text widget to display the file path
        self.text = tk.Text(self)
        self.text.pack()

    def select_file(self):
        # Open the file selection dialog
        filename = filedialog.askopenfilename()

        # Get the full path of the selected file
        filepath = os.path.abspath(filename)

        # Display the file path on the text widget
        self.text.delete("1.0", tk.END)
        self.text.insert("1.0", filepath)


if __name__ == "__main__":

    # Create an instance of the App class
    app = App()

    # Start the mainloop
    app.mainloop()