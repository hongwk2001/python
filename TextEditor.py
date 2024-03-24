import tkinter as tk

class TextEditor(tk.Frame):
    def __init__(self, master):
        super().__init__(master)

        self.text = tk.Text(self)
        self.text.pack()

        self.scroll = tk.Scrollbar(self)
        self.scroll.config(command=self.text.yview)
        self.text.config(yscrollcommand=self.scroll.set)
        self.scroll.pack(side=tk.RIGHT, fill=tk.Y)

        self.menu = tk.Menu(self)
        self.master.config(menu=self.menu)

        self.file_menu = tk.Menu(self.menu)
        self.menu.add_cascade(label="File", menu=self.file_menu)
        self.file_menu.add_command(label="New", command=self.new_file)
        self.file_menu.add_command(label="Open", command=self.open_file)
        self.file_menu.add_command(label="Save", command=self.save_file)
        self.file_menu.add_command(label="Exit", command=self.quit)

        self.edit_menu = tk.Menu(self.menu)
        self.menu.add_cascade(label="Edit", menu=self.edit_menu)
        self.edit_menu.add_command(label="Undo", command=self.undo)
        self.edit_menu.add_command(label="Redo", command=self.redo)
        self.edit_menu.add_command(label="Cut", command=self.cut)
        self.edit_menu.add_command(label="Copy", command=self.copy)
        self.edit_menu.add_command(label="Paste", command=self.paste)

    def new_file(self):
        self.text.delete("1.0", tk.END)

    def open_file(self):
        file = tk.filedialog.askopenfile(mode="r")
        if file:
            self.text.delete("1.0", tk.END)
            self.text.insert("1.0", file.read())

    def save_file(self):
        file = tk.filedialog.asksaveasfile(mode="w")
        if file:
            file.write(self.text.get("1.0", tk.END))

    def quit(self):
        self.master.destroy()

    def undo(self):
        self.text.edit_undo()

    def redo(self):
        self.text.edit_redo()

    def cut(self):
        self.text.clipboard_clear()
        self.text.delete("sel.first", "sel.last")

    def copy(self):
        self.text.clipboard_append(self.text.get("sel.first", "sel.last"))

    def paste(self):
        self.text.insert("insert", self.text.clipboard_get())


if __name__ == "__main__":
    root = tk.Tk()
    text_editor = TextEditor(root)
    text_editor.pack()
    root.mainloop()