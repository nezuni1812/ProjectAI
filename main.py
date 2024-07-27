import PathFinder
import Visualizer
import ReadInput
import tkinter as tk

def main():
    file_path = 'input.txt'
    n, m, time_limit, fuel_capacity, maze_grid, maze, starts, goals = ReadInput.read_input_file(file_path)

    start = starts[0]  # Starting point 'S'
    goal = goals[0]  # Goal point 'G'
    
    visualizer = Visualizer.Visualizer()

    # Level 1 Test 
    
    bfs_finder  = PathFinder.BFSPathFinder(maze, visualizer)
    dfs_finder  = PathFinder.DFSPathFinder(maze, visualizer)
    ucs_finder  = PathFinder.UCSPathFinder(maze, visualizer)
    gbfs_finder = PathFinder.GBFSPathFinder(maze, visualizer)
    a_star_finder = PathFinder.AStarPathFinder(maze, visualizer)

    visualizer.root.update()
    visualizer.root.after(400)
    bfs_finder.visualizer.set_map(maze_grid)
    bfs_finder.visualizer.make_boxes()
    bfs_finder.visualizer.draw_screen()
    
    print("Running BFS...")
    #bfs_finder.start_visualizer(start, goal)
    visualizer.root.after(300)
    
    print("\nRunning DFS...")
    dfs_finder.start_visualizer(start, goal)
    visualizer.root.after(300)
    
    print("\nRunning UCS...")
    ucs_finder.start_visualizer(start, goal)
    visualizer.root.after(300)

    print("\nRunning GBFS...")
    gbfs_finder.start_visualizer(start, goal)
    visualizer.root.after(300)

    print("\nRunning A*...")
    a_star_finder.start_visualizer(start, goal)
    visualizer.root.after(300)


    # Level 2 Test
    #level2_finder = PathFinder.PathFinderLevel2(maze, visualizer)
    #level2_finder.set_time_limit(time_limit)
    #level2_finder.visualizer.set_map(maze_grid)
    
    print("\nRunning A*_Level 2...")
    #level2_finder.start_visualizer(start, goal)
    # Make the screen stay alive
    #level2_finder.visualizer.root.mainloop()

if __name__ == "__main__":
    main()