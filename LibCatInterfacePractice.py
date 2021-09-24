from tkinter import *
from tkinter import ttk

# ttk does not have background colour, try style.
# by default widgets are placed in the centre of the cell they are in. stick takes a string which can move the position
# of the widget in the cell. If you set to stick to all areas go stick = 'nsew'; this will not make it repsonsive the cells will
# only size to the smallest possible size

# .pack(fill = BOTH)

root = Tk()

root.title('Frame Practice')
root.geometry("500x250")
root.geometry("+800+450")  # position of window in the screen

# root.rowconfigure(0, weight = 1)
# root.rowconfigure(1, weight = 1)
# root.grid_columnconfigure(0, weight=1)

root.columnconfigure(0, weight = 1)
root.columnconfigure(1, weight = 1)
root.columnconfigure(2, weight = 1)
root.columnconfigure(3, weight = 1)

frame1 = ttk.Frame(root)
frame2 = ttk.Frame(root)
frame3 = ttk.Frame(root)
frame4 = ttk.Frame(root)

frame1.config(height = 10, width = 20, relief = RIDGE)
frame2.config(height = 10, width = 20, relief = RIDGE)
frame3.config(height = 10, width = 20, relief = RIDGE)
frame4.config(height = 10, width = 20, relief = RIDGE)

frame1.grid(row=0, column = 0, stick = 'nsew')
frame2.grid(row=0, column = 1, stick = 'nsew')
frame3.grid(row=0, column = 2, stick = 'nsew')
frame4.grid(row=0, column = 3, stick = 'nsew')

text1 = Text(frame1, bg='#112233', fg='white', height = 20, width = 20) #  default text box seems to be quite large, but you can specify size
text2 = Text(frame2, bg='#112233', fg='white', height = 10, width = 20)
text3 = Text(frame3, bg='#112233', fg='white', height = 10, width = 20)
text4 = Text(frame4, bg='#112233', fg='white', height = 10, width = 20)

text1.pack(fill = BOTH)
text2.pack(fill = BOTH)
text3.pack(fill = BOTH)
text4.pack(fill = BOTH)


root.mainloop()

