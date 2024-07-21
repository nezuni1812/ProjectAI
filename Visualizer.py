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
    # Declare all attributes, CONSTs, variables
    def __init__(self, map: list = None, init_func = None) -> None:
        if map is None:
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
        
        self.toggle = True
        self.toggleCurrent = True
        
        self.BOX_WIDTH = 50
        self.PAD = 3
        
        self.colors = {
            0: '#fff',
            -1: '#647687',
            'S': '#d5e8d4',
            'G': '#f8cecc',
            'F': '#fff2cc',
        }
        
        self.root = Tk()
        self.root.geometry('520x600')
        self.root.configure(background='#696969')
        
        self.canvas = Canvas()
        self.canvas.pack(fill='both', expand=True)
        
        self.make_boxes()
        self.canvas.pack()

        pass
    
    def set_map(self, map: list):
        self.maze = map
    
    def draw_screen(self):
        self.canvas.pack()
        self.root.update()
    
    # def draw(self):
    #     print('Drawing...')
    #     self.root = Tk()
    #     self.root.geometry('520x600')
    #     self.root.configure(background='#696969')

    #     self.canvas = Canvas()
    #     self.canvas.pack(fill='both', expand=True)
        
    #     self.make_boxes()
    #     self.canvas.pack()
    #     ttk.Button(text='Start path finding', command=self.start_func).pack()

    #     self.root.mainloop()

    def update_frontier(self, frontier: list):
        for j, i in frontier:
            x0 = i*self.BOX_WIDTH + self.PAD
            y0 = j*self.BOX_WIDTH + self.PAD
            x1 = (i + 1)*self.BOX_WIDTH + self.PAD
            y1 = (j + 1)*self.BOX_WIDTH + self.PAD
            
            self.canvas.create_rectangle(x0, y0, x1, y1, fill='#e4f6d4', width=1)
            self.canvas.create_text(x0 + self.BOX_WIDTH/2, y0 + self.BOX_WIDTH/2, text=self.maze[j][i], font=('Cascadia Code', 14))
            
    def update_path(self, path: list):
        self.make_boxes()
        
        for j, i in path:
            x0 = i*self.BOX_WIDTH + self.PAD
            y0 = j*self.BOX_WIDTH + self.PAD
            x1 = (i + 1)*self.BOX_WIDTH + self.PAD
            y1 = (j + 1)*self.BOX_WIDTH + self.PAD
            
            self.canvas.create_rectangle(x0, y0, x1, y1, fill='#e4f6d4', width=1)
            self.canvas.create_text(x0 + self.BOX_WIDTH/2, y0 + self.BOX_WIDTH/2, text=self.maze[j][i], font=('Cascadia Code', 14))
            
    def update_current(self, current):
        j, i = current
        x0 = i*self.BOX_WIDTH + self.PAD
        y0 = j*self.BOX_WIDTH + self.PAD
        x1 = (i + 1)*self.BOX_WIDTH + self.PAD
        y1 = (j + 1)*self.BOX_WIDTH + self.PAD
        
        self.canvas.create_rectangle(x0, y0, x1, y1, fill='#f8cecc', width=1.4)
        self.canvas.create_text(x0 + self.BOX_WIDTH/2, y0 + self.BOX_WIDTH/2, text=self.maze[j][i], font=('Cascadia Code', 14))
        pass

    def make_boxes(self):
        for j, _ in enumerate(self.maze):
            for i, _ in enumerate(self.maze[0]):
                x0 = i*self.BOX_WIDTH + self.PAD
                y0 = j*self.BOX_WIDTH + self.PAD
                x1 = (i + 1)*self.BOX_WIDTH + self.PAD
                y1 = (j + 1)*self.BOX_WIDTH + self.PAD
                if (self.maze[j][i] in self.colors):
                    self.canvas.create_rectangle(x0, y0, x1, y1, fill=self.colors[self.maze[j][i]], width=1)
                elif (isinstance(self.maze[j][i], str) and any(c.isalpha() for c in self.maze[j][i])):
                    self.canvas.create_rectangle(x0, y0, x1, y1, fill=self.colors[self.maze[j][i][0]], width=1)
                    self.canvas.create_text(x0 + self.BOX_WIDTH/2, y0 + self.BOX_WIDTH/2, text=self.maze[j][i], font=('Cascadia Code', 14))
                else:
                    self.canvas.create_rectangle(x0, y0, x1, y1, fill='#dae8fc', width=1)
                    self.canvas.create_text(x0 + self.BOX_WIDTH/2, y0 + self.BOX_WIDTH/2, text=self.maze[j][i], font=('Cascadia Code', 14))

    
def main():
    visuals = Visualizer()
    # visuals.draw()

if __name__ == '__main__':
    # start_reloader()
    main()