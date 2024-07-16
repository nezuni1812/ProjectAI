import hupper
from tkinter import *
from tkinter import ttk

BOX_WIDTH = 50
PAD = 3

def start_reloader():
    reloader = hupper.start_reloader('mian.main')

colors = {
    0: '#fff',
    -1: '#647687',
    'S': '#d5e8d4',
    'G': '#f8cecc',
    'F': '#fff2cc',
}

def make_boxes(canv: Canvas):
    maze = [
        [0, 0, 0, -1, -1, 0, 0, 0, 0, 0],
        [0, 'S', 0, 0, 0, 0, 0, -1, 0, -1],
        [0, 0, -1, -1, -1, 'S1', 0, -1, 0, -1],
        [0, 0, 0, 0, -1, 0, 0, -1, 0, 0],
        [0, 0, -1, -1, -1, 0, 'G2', -1, -1, 0],
        [1, 0, -1, 0, 0, 0, 0, 0, -1, 0],
        [0, 0, 'F1', 0, -1, 4, -1, 8, -1, 0],
        [0, 0, 0, 0, -1, 0, 0, 0, 'G', 0],
        [0, -1, -1, -1, -1, 'S2', 0, 0, 0, 0],
        ['G1', 0, 5, 0, 0, 0, -1, -1, -1, 0],
    ]
    # canv.create_rectangle(0, 0, 24, 24, fill='yellow', width=1)
    # canv.create_rectangle(24, 0, 48, 24, fill='red', width=1)
    for j, _ in enumerate(maze):
        for i, _ in enumerate(maze[0]):
            x0 = i*BOX_WIDTH + PAD
            y0 = j*BOX_WIDTH + PAD
            x1 = (i + 1)*BOX_WIDTH + PAD
            y1 = (j + 1)*BOX_WIDTH + PAD
            if (maze[j][i] in colors):
                canv.create_rectangle(x0, y0, x1, y1, fill=colors[maze[j][i]], width=1)
            elif (isinstance(maze[j][i], str) and any(c.isalpha() for c in maze[j][i])):
                canv.create_rectangle(x0, y0, x1, y1, fill=colors[maze[j][i][0]], width=1)
                canv.create_text(x0 + BOX_WIDTH/2, y0 + BOX_WIDTH/2, text=maze[j][i], font=('Times New Roman', 14))
            else:
                canv.create_rectangle(x0, y0, x1, y1, fill='#dae8fc', width=1)
                canv.create_text(x0 + BOX_WIDTH/2, y0 + BOX_WIDTH/2, text=maze[j][i], font=('Times New Roman', 14))
    canv.pack()

def main():
    root = Tk()
    root.geometry('520x600')
    root.configure(background='#696969')
    # root.option_add("*Button*Background", "#696969") 


    # greeting = Label(text="Hello, Tkinter")
    # greeting.pack()
    # thing = ttk.Label(text="Hi")
    # thing.pack()
    # ttk.Button(text='Press me here').pack()

    canvas = Canvas()
    canvas.pack(fill='both', expand=True)
    
    make_boxes(canvas)

    root.mainloop()

if __name__ == '__main__':
    start_reloader()
    main()