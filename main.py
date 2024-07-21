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


    bfs_finder = PathFinder.BFSPathFinder(maze_grid, visualizer)
    gbfs_finder = PathFinder.GBFSPathFinder(maze_grid, visualizer)

    print("Running BFS...")
    bfs_finder.start_visualizer(start, goal)

    print("\nRunning GBFS...")
    gbfs_finder.start_visualizer(start, goal)

if __name__ == "__main__":
    main()