import time
import hupper
import pyglet
from tkinter import *
from tkinter import ttk
from ctypes import windll
from PIL import Image, ImageTk

# Make texts sharper
windll.shcore.SetProcessDpiAwareness(1)

# Add font file
pyglet.font.add_file('CascadiaCode.ttf')


def start_reloader():
    reloader = hupper.start_reloader('mian.main')

move = True

class Visualizer:
    # Declare all attributes, CONSTs, variables
    def __init__(self, map: list = None, init_func = None) -> None:
        if map is None:
            self.maze = []
        else:
            self.maze = map
        
        self.toggle = True
        self.toggleCurrent = True
        
        self.BOX_WIDTH = 50
        self.PAD = 3
        
        self.colors = {
            "0": '#fff',
            "-1": '#647687',
            'S': '#d5e8d4',
            'G': '#f8cecc',
            'F': '#fff2cc',
        }
        
        self.root = Tk()
        self.root.geometry('980x650')
        self.root.configure(background='#696969')
        
        self.canvas = Canvas()
        self.canvas.pack(fill='both', expand=True)
        
        self.make_boxes()
        self.canvas.pack()
        self.images = []

        pass
    
    def set_map(self, map: list):
        self.maze = map
    
    def draw_screen(self):
        # start = time.time()
        self.canvas.pack()
        self.root.update()
        # print('Draw:', time.time() - start)
        
    def create_transparent_rectangle(self, x1, y1, x2, y2, **kwargs):
        transparent_image = None
        if 'alpha' in kwargs:
            alpha = int(kwargs.pop('alpha') * 255)
            fill = kwargs.pop('fill')
            fill = self.root.winfo_rgb(fill) + (alpha,)
            image = Image.new('RGBA', (x2-x1, y2-y1), fill)
            self.images.append(ImageTk.PhotoImage(image))
            transparent_image = self.canvas.create_image(x1, y1, image=self.images[-1], anchor='nw')
        if transparent_image is not None:
            return transparent_image
        return self.canvas.create_rectangle(x1, y1, x2, y2, **kwargs)
    
    def next(self):
        self.move = not self.move
        print(self.move)
    
    def toggle_autoplay(self):
        if self.autoplay == False:
            self.move = True
        self.autoplay = not self.autoplay
    
    def draw_path_turn_based(self, path: list):
        agent_colrs = {
            'S' : '#10e305',
            'S1': '#9b08e4',
            'S2': '#a4ef04',
            'S3': '#f71c03',
            'S4': '#036af9',
            'S5': '#f6ba05',
            'S6': '#04faa4',
            'S7': '#02c4e7',
            'S8': '#f98202'
        }
        colrs = {
            'S': 'red',
            'S1': 'blue',
            'S2': 'green',
            'S3': 'purple',
            'S4': 'orange',
            'S5': '#fff2cc',
            'S6': '#f8cecc',
            'S7': '#d0e0e3',
            'S8': '#ffe6cc'
        }
        
        txt = self.canvas.create_text(450, 50, text='Step', font=('Cascadia Code', 14), anchor='nw')
        self.canvas.create_text(450, 120, text='<Arrow right> for next move\n<Enter> for autoplay', font=('Cascadia Code', 14), anchor='nw')
        self.canvas.itemconfigure(txt, text = 'hey')
        
        self.move = True
        self.autoplay = False
        
        self.root.bind("<Return>", lambda *args: self.toggle_autoplay())
        self.root.bind("<Right>", lambda *args: self.next())
        # btton = Button(self.root, text='Next move', command=lambda *args: self.next())
        # btton.place(x=65, y=100)
        
        # self.root.mainloop()
        
        for step in path:
            # Position for current node
            j, i = step[2]
            x0 = i*self.BOX_WIDTH + self.PAD
            y0 = j*self.BOX_WIDTH + self.PAD
            x1 = (i + 1)*self.BOX_WIDTH + self.PAD
            y1 = (j + 1)*self.BOX_WIDTH + self.PAD
            
            # Position for placing previouse outline
            before_j, before_i = step[1]
            before_x0 = before_i*self.BOX_WIDTH + self.PAD
            before_y0 = before_j*self.BOX_WIDTH + self.PAD
            before_x1 = (before_i + 1)*self.BOX_WIDTH + self.PAD
            before_y1 = (before_j + 1)*self.BOX_WIDTH + self.PAD
            
            curren_box = self.create_transparent_rectangle(x0, y0, x1, y1, fill=colrs[step[0]], width=1, alpha=.8)
            outline = self.canvas.create_rectangle(before_x0, before_y0, before_x1, before_y1, outline=colrs[step[0]], width=3)
            # outline = self.canvas.create_rectangle(x0, y0, x1, y1, outline='white', width=2)
            print(x0, y0, x1, y1)
            print(before_x0, before_y0, before_x1, before_y1)
            print(self.canvas.coords(outline))
            while (self.canvas.coords(outline)[0] != x0 or self.canvas.coords(outline)[1] != y0):
                x_amount = 1 if x0 > self.canvas.coords(outline)[0] else -1 if x0 < self.canvas.coords(outline)[0] else 0
                y_amount = 1 if y0 > self.canvas.coords(outline)[1] else -1 if y0 < self.canvas.coords(outline)[1] else 0
                self.canvas.move(outline, x_amount, y_amount)
                self.canvas.after(1)
                self.root.update()
                
            # self.canvas.delete('all')
            # self.canvas.move(outline, )
            self.canvas.create_text(x0 + self.BOX_WIDTH/2, y0 + self.BOX_WIDTH/2, text=step[0], font=('Cascadia Code', 14))
            
            self.canvas.itemconfigure(txt, text = f"Turn: {step[0]} - {step[3]}\n\
From {step[1][0], step[1][1]} to {step[2][0], step[2][1]}")
            
            self.draw_screen()
            self.move = False
                
            if self.autoplay:
                self.root.after(200)
                self.canvas.delete(curren_box)
                self.canvas.delete(outline)
                continue
            
            while not self.move:
                self.root.update()
            # time.sleep(0.4)
            self.canvas.delete(outline)
            self.canvas.delete(curren_box)
        
    
    def add_point(self, start, txt):
        print(start[0])
        print(start[1])
        self.maze[start[0]][start[1]] = txt
        print(self.maze[start[0]][start[1]])
        print(self.colors[self.maze[start[0]][start[1]][0]])
        print('--')
    
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