import PathFinder
import Visualizer
import ReadInput
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

import level_3_ui_implementation
import level_4_ui_implementation

index = 0

def level_1(visualizer, file_path):
    n, m, time_limit, fuel_capacity, maze_grid, maze, starts, goals = ReadInput.read_input_file(file_path)

    start = starts[0]  # Starting point 'S'
    goal = goals[0]  # Goal point 'G'
    
    bfs_finder  = PathFinder.BFSPathFinder(maze, visualizer)
    dfs_finder  = PathFinder.DFSPathFinder(maze, visualizer)
    ucs_finder  = PathFinder.UCSPathFinder(maze, visualizer)
    gbfs_finder = PathFinder.GBFSPathFinder(maze, visualizer)
    a_star_finder = PathFinder.AStarPathFinder(maze, visualizer)
    
    function_list = []
    def next_move(change_amount = 0):
        global index
        index = max(min(index + change_amount, len(function_list) - 1), 0)
        print(index)
        foo = function_list[index]
        foo()
        
    for ele in visualizer.root.winfo_children():
        if not isinstance(ele, tk.Canvas):
            ele.destroy()
    visualizer.canvas.pack(fill='both', expand=True)
        
    # Add key binds
    visualizer.root.unbind('<Return')
    visualizer.root.bind("<Return>", lambda *args: next_move())
    visualizer.root.bind("<Right>", lambda *args: next_move(1))
    visualizer.root.bind("<Left>", lambda *args: next_move(-1))

    visualizer.root.update()
    visualizer.root.after(400)
    bfs_finder.visualizer.set_map(maze_grid)
    bfs_finder.visualizer.make_boxes()
    bfs_finder.visualizer.draw_screen()
    # Instruction
    lef_padding = len(maze[0]) * 50 + 20
    visualizer.canvas.create_text(lef_padding, 12, text='Level 1: Basic', font=('Cascadia Code', 14, 'bold'), anchor='nw')
    visualizer.canvas.create_text(lef_padding, 100, text='<Arrow ◀ ▶> to change algorithm\n<Enter ⏎> to start the algorithm', font=('Cascadia Code', 14), anchor='nw')
    
    def bfs():
        print("Running BFS...")
        bfs_finder.start_visualizer(start, goal)
    function_list.append(bfs)
    
    def dfs():
        print("\nRunning DFS...")
        dfs_finder.start_visualizer(start, goal)
    function_list.append(dfs)
    
    def ucs():
        print("\nRunning UCS...")
        ucs_finder.start_visualizer(start, goal)
    function_list.append(ucs)

    def gbfs():
        print("\nRunning GBFS...")
        gbfs_finder.start_visualizer(start, goal)
    function_list.append(gbfs)

    def A():
        print("\nRunning A*...")
        a_star_finder.start_visualizer(start, goal)
    function_list.append(A)
        
    # visualizer.root.mainloop()

def level_2(visualizer, file_path):
    n, m, time_limit, fuel_capacity, maze_grid, maze, starts, goals = ReadInput.read_input_file(file_path)
    
    for ele in visualizer.root.winfo_children():
        if not isinstance(ele, tk.Canvas):
            ele.destroy()
    visualizer.canvas.pack(fill='both', expand=True)
    
    visualizer.root.unbind('<Return')
    visualizer.root.bind("<Return>", lambda *args: level_2(visualizer, file_path))
    
    start = starts[0]  # Starting point 'S'
    goal = goals[0]  # Goal point 'G'
    
    # Level 2 Test
    level2_finder = PathFinder.PathFinderLevel2(maze, visualizer)
    level2_finder.set_time_limit(time_limit)
    level2_finder.visualizer.set_map(maze_grid)
    
    print("\nRunning A*_Level 2...")
    level2_finder.start_visualizer(start, goal)
    # Make the screen stay alive
    # level2_finder.visualizer.root.mainloop()

def level_4(visualizer, file_path):
    for ele in visualizer.root.winfo_children():
        if not isinstance(ele, tk.Canvas):
            ele.destroy()
    visualizer.canvas.pack_forget()

    def chose_file():
        visualizer.canvas.pack(fill='both', expand=True)
        visualizer.root.unbind('<Return')
        visualizer.root.bind("<Return>", lambda *args: level_4(visualizer, file_path))
        drop.destroy()
        button.destroy()
        level_4_ui_implementation.level_4(visualizer, clicked.get())
        print('File:', clicked.get())
        
    options = [ 
        "input1_level4.txt", 
        "input2_level4.txt", 
        "input3_level4.txt", 
        "input4_level4.txt",
        "input5_level4.txt", 
        "input6_level4.txt" 
    ] 
    clicked = tk.StringVar()
    clicked.set("input1_level4.txt") 
    drop = ttk.OptionMenu(visualizer.root , clicked , *options ) 
    drop.pack()
    button = ttk.Button(visualizer.root , text="Run this file for Level 4" , command=chose_file)
    button.pack()
    

level_list = []
level_index = 0
if __name__ == "__main__":
    visualizer = Visualizer.Visualizer()
    
    level_list.append(lambda *args: level_1(visualizer, 'input5_level1.txt'))
    level_list.append(lambda *args: level_2(visualizer, 'input5_level2.txt'))
    level_list.append(lambda *args: level_3_ui_implementation.level_3(visualizer, 'input5_level3.txt'))
    level_list.append(lambda *args: level_4(visualizer, 'input1_level4.txt'))
    
    def change_level(new_level = None):
        global level_index
        if new_level is not None:
            level_index = max(min(new_level, len(level_list) - 1), 0)
        print(level_index)
        foo = level_list[level_index]
        visualizer.canvas.delete('all')
        foo()
        
    visualizer.canvas.create_text(10, 12, text='Using number key 1, 2, 3, 4 to change level', font=('Cascadia Code', 14), anchor='nw')
    img= ImageTk.PhotoImage(Image.open("images/welcome.png").resize((1100, 680)))
    visualizer.canvas.create_image(0, 30, image=img, anchor='nw')
        
    visualizer.root.bind("<Key-1>", lambda *args: change_level(0))
    visualizer.root.bind("<Key-2>", lambda *args: change_level(1))
    visualizer.root.bind("<Key-3>", lambda *args: change_level(2))
    visualizer.root.bind("<Key-4>", lambda *args: change_level(3))
    
    visualizer.root.mainloop()