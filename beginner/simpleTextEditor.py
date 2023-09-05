import tkinter as tk
from tkinter import filedialog

root = tk.Tk()
root.title('Simple Text Editor')
root.geometry('800x600')

text_widget = tk.Text(root)
text_widget.pack(fill=tk.BOTH, expand=True)

def openFile():
    file_path = filedialog.askopenfilename()
    if file_path:
        with open(file_path, 'r') as f:
            text_widget.delete("1.0", tk.END)
            text_widget.insert(tk.END, f.read())
            
def saveFile():
    file_path = filedialog.asksaveasfilename(defaultextension=".txt")
    if file_path:
        with open(file_path, "w") as f:
            f.write(text_widget.get("1.0", tk.END))
            
def quitApp():
    root.quit()
    
menu_bar = tk.Menu(root)
root.config(menu=menu_bar)

file_menu = tk.Menu(menu_bar)
menu_bar.add_cascade(label="File", menu=file_menu)
menu_bar.add_command(label="Open", command=openFile)
menu_bar.add_command(label="Save", command=saveFile)
file_menu.add_separator()
file_menu.add_command(label="Quit", command=quitApp)

root.mainloop()