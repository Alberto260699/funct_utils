#python -m tkinter comando di prova, apre una finestra di prova
#tkinter libreria per aprire finestre, come quelle dei grafici che possono essere rese interattive
from tkinter import *
from tkinter import messagebox
import random

def no():
	messagebox.showinfo('', 'Thanks bro')
	quit()

def motionMouse():
	btnYes.place(x=random.randint(0, 500), y=random.randint(0, 500))

root=Tk()
root.geometry('600x600')
root.title('survey')
root.resizable(width=False, height=False)
root['bg']='white'

label=Label(root, text='Are you gay?', font='Arial 20 bold', bg='white').pack()
btnYes=Button(root, text='No', font='Arial 20 bold', command=motionMouse)
btnYes.place(x=170, y=100)
btnNo=Button(root, text='Yes', font='Arial 20 bold', command=no).place(x=350, y=100)

root.mainloop()

#--------------------------------------------------------------------------------------------

# Import all files from
# tkinter and overwrite
# all the tkinter files
# by tkinter.ttk
from tkinter import *
from tkinter.ttk import *

# creates tkinter window or root window
root = Tk()
root.geometry('200x100')

# function to be called when mouse enters in a frame
def enter(event):
	print('Button-2 pressed at x = % d, y = % d'%(event.x, event.y))

# function to be called when mouse exits the frame
def exit_(event):
	print('Button-3 pressed at x = % d, y = % d'%(event.x, event.y))

# frame with fixed geometry
frame1 = Frame(root, height = 100, width = 200)

# these lines are showing the
# working of bind function
# it is universal widget method
frame1.bind('<Enter>', enter)
frame1.bind('<Leave>', exit_)

frame1.pack()

mainloop()

#--------------------------------------------------------------------------------------------

# Import all files from
# tkinter and overwrite
# all the tkinter files
# by tkinter.ttk
from tkinter import *
from tkinter.ttk import *

# creates tkinter window or root window
root = Tk()
root.geometry('200x100')

# function to be called when button-2 of mouse is pressed
def pressed2(event):
	print('Button-2 pressed at x = % d, y = % d'%(event.x, event.y))

# function to be called when button-3 of mouse is pressed
def pressed3(event):
	print('Button-3 pressed at x = % d, y = % d'%(event.x, event.y))

## function to be called when button-1 is double clocked
def double_click(event):
	print('Double clicked at x = % d, y = % d'%(event.x, event.y))

frame1 = Frame(root, height = 100, width = 200)

# these lines are binding mouse
# buttons with the Frame widget
frame1.bind('<Button-2>', pressed2)
frame1.bind('<Button-3>', pressed3)
frame1.bind('<Double 1>', double_click)

frame1.pack()

mainloop()

#--------------------------------------------------------------------------------------------

from tkinter import *

def my_fun():
	print("Function called")
	

win = Tk()

button = Button(win, text="Click me", command = my_fun)
button.pack()

win.mainloop()

#--------------------------------------------------------------------------------------------

from tkinter import *

root = Tk()
root.title("Tip & Bill Calculator")

totaltxt = Label(root, text="Total", font=("Helvitca", 16))
tiptxt = Label(root, text="Tip (%)", font=("Helvitca", 16))
peopletxt = Label(root, text="people", font=("Helvitca", 16))

totaltxt.grid(row=0, column=0, sticky=E)
tiptxt.grid(row=1, column=0, sticky=E)
peopletxt.grid(row=2, column=0, sticky=E)

totalentry = Entry(root)
tipentry = Entry(root)
peopleentry = Entry(root)

totalentry.grid(row=0, column=1)
tipentry.grid(row=1, column=1)
peopleentry.grid(row=2, column=1)

ans = Label(root, text = "ANS")
ans.grid(row=4, column=0, columnspan=2, sticky=W)

def answer():
	total = totalentry.get()
	tip = tipentry.get()
	people = peopleentry.get()
	if not (total and tip):
		ans['text'] = 'Enter total and tip as non-0 numbers'
	else:
		total = float(total)
		tip = float(tip) / 100
		people = int(people) if people else 1
		ans['text'] = str(round(total * tip / people, 2)) + " per person"

calc = Button(root, text ="Calculate", fg = "black", command = answer)
calc.grid(row=3, column=1)

root.mainloop()