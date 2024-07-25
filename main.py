import PathFinder
import Visualizer
import ReadInput

def main():
    file_path = 'input1_level2.txt'
    n, m, time_limit, fuel_capacity, maze_grid, positions = ReadInput.read_input_file(file_path)

    start = positions['S']  # Starting point 'S'
    goal = positions['G']  # Goal point 'G'
    
    visualizer = Visualizer.Visualizer()

    # Level 1 Test 
    bfs_finder  = PathFinder.BFSPathFinder(maze_grid, visualizer)
    dfs_finder  = PathFinder.DFSPathFinder(maze_grid, visualizer)
    ucs_finder  = PathFinder.UCSPathFinder(maze_grid, visualizer)
    gbfs_finder = PathFinder.GBFSPathFinder(maze_grid, visualizer)
    a_star_finder = PathFinder.AStarPathFinder(maze_grid, visualizer)

    # print("Running BFS...")
    # bfs_finder.visualizer.set_map(maze_grid)
    # bfs_finder.start_visualizer(start, goal)

    # print("\nRunning DFS...")
    # dfs_finder.start_visualizer(start, goal)

    # print("\nRunning UCS...")
    # ucs_finder.start_visualizer(start, goal)

    # print("\nRunning GBFS...")
    # gbfs_finder.start_visualizer(start, goal)

    # print("\nRunning A*...")
    # a_star_finder.start_visualizer(start, goal)

    # Level 2 Test
    level2_finder = PathFinder.PathFinderLevel2(maze_grid, visualizer)
    level2_finder.set_time_limit(time_limit)
    level2_finder.visualizer.set_map(maze_grid)
    
    print("\nRunning A*_Level 2...")
    level2_finder.start_visualizer(start, goal)
    # Make the screen stay alive
    level2_finder.visualizer.root.mainloop()

if __name__ == "__main__":
    main()