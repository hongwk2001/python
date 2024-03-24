from tkinter import *
from tkinter import ttk


appln = Tk()
appln.title("Application for GUI to represent the University ")
ttk.Label(appln, text ="Treeview(hierarchical)").pack()
treeview = ttk.Treeview(appln)
treeview.pack()
root=treeview.insert('', 0, text ='Korea')
treeview.insert(root, 0, text ='seoul')
treeview.insert(root, 2, text ='Taejeon')
treeview.insert(root, 1, text ='Pusan')

def item_selected(event):
    print(treeview.selection()[0])
    for item in treeview.selection():
         print(item, type(item), treeview.item(item, "text"))

# Bind the <<TreeviewSelect>> event to the callback function
treeview.bind("<<TreeviewSelect>>", item_selected)

appln.mainloop()