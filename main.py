import PathFinder
import Visualizer
import ReadInput
import tkinter as tk

index = 0

def level_1(visualizer, file_path):
    n, m, time_limit, fuel_capacity, maze_grid, maze, starts, goals = ReadInput.read_input_file(file_path)

    start = starts[0]  # Starting point 'S'
    goal = goals[0]  # Goal point 'G'
    
    # Level 1 Test 
    
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
        
    visualizer.root.bind("<Return>", lambda *args: next_move())
    visualizer.root.bind("<Right>", lambda *args: next_move(1))
    visualizer.root.bind("<Left>", lambda *args: next_move(-1))

    visualizer.root.update()
    visualizer.root.after(400)
    bfs_finder.visualizer.set_map(maze_grid)
    bfs_finder.visualizer.make_boxes()
    bfs_finder.visualizer.draw_screen()
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

level_list = []
level_index = 0
if __name__ == "__main__":
    visualizer = Visualizer.Visualizer()
    file_path = 'input2_level1.txt'
    
    # level_1(visualizer, file_path)
    level_list.append(lambda *args: level_1(visualizer, file_path))
    level_list.append(lambda *args: level_2(visualizer, file_path))
    
    def change_level(new_level = 0):
        global level_index
        level_index = max(min(new_level, len(level_list) - 1), 0)
        print(level_index)
        foo = level_list[level_index]
        visualizer.canvas.delete('all')
        foo()
        
    visualizer.canvas.create_text(10, 12, text='Using number key 1, 2, 3, 4 to change level', font=('Cascadia Code', 14), anchor='nw')
        
    visualizer.root.bind("<Key-1>", lambda *args: change_level(0))
    visualizer.root.bind("<Key-2>", lambda *args: change_level(1))
    visualizer.root.bind("<Key-3>", lambda *args: change_level(2))
    visualizer.root.mainloop()