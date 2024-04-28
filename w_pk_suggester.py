
import sys
import tkinter as tk
import load_csv_to_sqlite_then_find_uniq_combination as lcts
from tkinter import filedialog

class StdoutRedirector(object):
    def __init__(self,text_widget):
        self.text_space = text_widget

    def write(self,string):
        self.text_space.insert('end', string)
        self.text_space.see('end')

def select_csv_file():
    csv_file_path = filedialog.askopenfilename(title="select csv file", filetypes=[("csv with header", "*.csv")])
    print(csv_file_path)

    db_path =  lcts.csv_to_db(csv_file_path)

    #as test
    if db_path:
        lcts.show_data(db_path)

    #only when successfull
    if db_path :
        lcts.find_uniq_combination(db_path)

class CoreGUI(object):
    def __init__(self,parent):
        self.parent = parent
        self.InitUI()

    def main(self):
        print('whatever')

    def InitUI(self):
        self.text_box = tk.Text(self.parent, wrap='word', height = 11, width=50)
        self.text_box.pack(expand=True, fill='both')
        sys.stdout = StdoutRedirector(self.text_box)

if __name__ =="__main__":
    app = tk.Tk()
    app.title("Primary Key suggester")
    tk.Label(app, text ="Plese select a csv file").pack()

    btn_select_csv=tk.Button(app, text="Select a CSV file", command=select_csv_file)
    btn_select_csv.pack()

    gui = CoreGUI(app)

    app.mainloop()