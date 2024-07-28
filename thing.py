from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk

root = Tk()

def show(): 
    label.config( text = clicked.get() ) 
    print(clicked.get())
  
# Dropdown menu options 
options = [ 
    "Monday", 
    "Tuesday", 
    "Wednesday", 
    "Thursday", 
    "Friday", 
    "Saturday", 
    "Sunday"
] 
  
# datatype of menu text 
clicked = StringVar() 
  
# initial menu text 
clicked.set( "Monday" ) 
  
# Create Dropdown menu 
drop = ttk.OptionMenu( root , clicked , *options ) 
drop.pack() 
  
# Create button, it will change label text 
button = ttk.Button( root , text = "click Me" , command = show ).pack() 
  
# Create Label 
label = ttk.Label( root , text = " " ) 
label.pack() 
  
# Execute tkinter 
root.mainloop() 
