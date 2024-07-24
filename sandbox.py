from tkinter import *

count = 800
def animate():
    c.move(ball, 6, 0)
    # if count <= 0:
    #     return
    # root.after(33, animate)

root = Tk()
c = Canvas(root, width = 200, height = 100)
c.pack()
ball = c.create_oval(0, 25, 50, 75)
animate()
root.mainloop()