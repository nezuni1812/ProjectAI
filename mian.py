import hupper
import pyglet
from tkinter import *
from tkinter import ttk
from ctypes import windll

# Make texts sharper
windll.shcore.SetProcessDpiAwareness(1)

# Add font file
pyglet.font.add_file('CascadiaCode.ttf')


def start_reloader():
    reloader = hupper.start_reloader('mian.main')


# maze = [
#     [0, 0, 0, -1, -1, 0, 0, 0, 0, 0],
#     [0, 'S', 0, 0, 0, 0, 0, -1, 0, -1],
#     [0, 0, -1, -1, -1, 'S1', 0, -1, 0, -1],
#     [0, 0, 0, 0, -1, 0, 0, -1, 0, 0],
#     [0, 0, -1, -1, -1, 0, 'G2', -1, -1, 0],
#     [1, 0, -1, 0, 0, 0, 0, 0, -1, 0],
#     [0, 0, 'F1', 0, -1, 4, -1, 8, -1, 0],
#     [0, 0, 0, 0, -1, 0, 0, 0, 'G', 0],
#     [0, -1, -1, -1, -1, 'S2', 0, 0, 0, 0],
#     ['G1', 0, 5, 0, 0, 0, -1, -1, -1, 0],
# ]

class Visualizer:
    def __init__(self) -> None:
        self.maze = [
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
        
        self.BOX_WIDTH = 50
        self.PAD = 3
        
        self.colors = {
            0: '#fff',
            -1: '#647687',
            'S': '#d5e8d4',
            'G': '#f8cecc',
            'F': '#fff2cc',
        }
        
        self.map1 = [
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
        self.map2 = [
            [0, 0, 0, 0, -1, -1, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, -1, 0, -1],
            [0, 0, -1, -1, -1, 0, 0, -1, 0, -1],
            [0, 0, 0, 0, -1, 0, 0, -1, 0, 0],
            [0, 0, -1, -1, -1, 0, 0, -1, -1, 0],
            [1, 0, -1, 0, 0, 0, 0, 0, -1, 0],
            [0, 0, 0, 0, -1, 4, -1, 8, -1, 0],
            [0, 0, 0, 0, -1, 0, 0, 0, 0, 0],
            [0, -1, -1, -1, -1, 0, 0, 0, 0, 0],
            [0, 0, 5, 0, 0, 0, -1, -1, -1, 0]
        ]

        self.root = Tk()
        self.root.geometry('520x600')
        self.root.configure(background='#696969')
        # self.root.option_add("*Button*Background", "#696969") 


        # greeting = Label(text="Hello, Tkinter")
        # greeting.pack()
        # thing = ttk.Label(text="Hi")
        # thing.pack()

        self.canvas = Canvas()
        self.canvas.pack(fill='both', expand=True)
        
        self.make_boxes(self.canvas)
        ttk.Button(text='Press me here', command=self.update_box).pack()

        self.root.mainloop()
        
        pass

    def make_boxes(self, canv: Canvas):
        # canv.create_rectangle(0, 0, 24, 24, fill='yellow', width=1)
        # canv.create_rectangle(24, 0, 48, 24, fill='red', width=1)
        for j, _ in enumerate(self.maze):
            for i, _ in enumerate(self.maze[0]):
                x0 = i*self.BOX_WIDTH + self.PAD
                y0 = j*self.BOX_WIDTH + self.PAD
                x1 = (i + 1)*self.BOX_WIDTH + self.PAD
                y1 = (j + 1)*self.BOX_WIDTH + self.PAD
                if (self.maze[j][i] in self.colors):
                    canv.create_rectangle(x0, y0, x1, y1, fill=self.colors[self.maze[j][i]], width=1)
                elif (isinstance(self.maze[j][i], str) and any(c.isalpha() for c in self.maze[j][i])):
                    canv.create_rectangle(x0, y0, x1, y1, fill=self.colors[self.maze[j][i][0]], width=1)
                    canv.create_text(x0 + self.BOX_WIDTH/2, y0 + self.BOX_WIDTH/2, text=self.maze[j][i], font=('Cascadia Code', 14))
                else:
                    canv.create_rectangle(x0, y0, x1, y1, fill='#dae8fc', width=1)
                    canv.create_text(x0 + self.BOX_WIDTH/2, y0 + self.BOX_WIDTH/2, text=self.maze[j][i], font=('Cascadia Code', 14))
        canv.pack()

    def update_box(self):
        if (self.maze == self.map1):
            self.maze = self.map2
        else:
            self.maze = self.map1
            
        print("Trying to update")
        self.make_boxes(self.canvas)
    
def main():
    visuals = Visualizer()

if __name__ == '__main__':
    # start_reloader()
    main()