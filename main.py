import PathFinder
import Visualizer

def main():
    maze_grid = [
        [0, 0, 0, 0, -1, -1, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, -1, 0, -1],
        [0, 0, -1, -1, -1, 0, 0, -1, 0, -1],
        [0, 0, 0, 0, -1, 0, 0, -1, 0, 0],
        [0, 0, -1, -1, -1, 0, 0, -1, -1, 0],
        [1, 0, -1, 0, 0, 0, 0, 0, -1, 0],
        [0, 0, -2, 0, -1, 4, -1, 8, -1, 0],
        [0, 0, 0, 0, -1, 0, 0, 0, 0, 0],
        [0, -1, -1, -1, -1, 0, 0, 0, 0, 0],
        [0, 0, 5, 0, 0, 0, -1, -1, -1, 0]
    ]

    visualizer = Visualizer.Visualizer()

    start = (1, 1)
    goal = (7, 8)

    # Level 1 Test 
    bfs_finder  = PathFinder.BFSPathFinder(maze_grid, visualizer)
    dfs_finder  = PathFinder.DFSPathFinder(maze_grid, visualizer)
    ucs_finder  = PathFinder.UCSPathFinder(maze_grid, visualizer)
    gbfs_finder = PathFinder.GBFSPathFinder(maze_grid, visualizer)
    a_star_finder = PathFinder.AStarPathFinder(maze_grid, visualizer)

    print("Running BFS...")
    bfs_finder.start_visualizer(start, goal)

    print("\nRunning DFS...")
    dfs_finder.start_visualizer(start, goal)

    print("\nRunning UCS...")
    ucs_finder.start_visualizer(start, goal)

    print("\nRunning GBFS...")
    gbfs_finder.start_visualizer(start, goal)

    print("\nRunning A*...")
    a_star_finder.start_visualizer(start, goal)

    # Level 2 Test
    level2_finder = PathFinder.PathFinderLevel2(maze_grid, visualizer)
    print("\nRunning A*_Level 2...")
    level2_finder.start_visualizer(start, goal)

if __name__ == "__main__":
    main()