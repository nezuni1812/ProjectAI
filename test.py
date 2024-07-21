import heapq
import time
from typing import List, Tuple, Dict, Set, Optional
from abc import ABC, abstractmethod
import Visualizer

class PriorityQueue:
    def __init__(self):
        self.elements = []
    
    def empty(self) -> bool:
        return len(self.elements) == 0
    
    def put(self, item, priority):
        heapq.heappush(self.elements, (priority, item))
    
    def get(self):
        return heapq.heappop(self.elements)[1]
    
    def list(self):
        return self.elements

class Maze:
    def __init__(self, grid: List[List[int]]):
        self.grid = grid
        self.height = len(grid)
        self.width = len(grid[0]) if self.height > 0 else 0

    def is_valid(self, x: int, y: int) -> bool:
        return 0 <= x < self.height and 0 <= y < self.width and self.grid[x][y] != -1

    def get_neighbors(self, current: Tuple[int, int]) -> List[Tuple[int, int]]:
        x, y = current
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        return [(x + dx, y + dy) for dx, dy in directions if self.is_valid(x + dx, y + dy)]

class PathFinder(ABC):
    def __init__(self, maze: Maze, visualizer: Visualizer.Visualizer):
        self.maze = maze
        self.visualizer = visualizer

    @staticmethod
    def manhattan_distance(a: Tuple[int, int], b: Tuple[int, int]) -> int:
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    @abstractmethod
    def find_path(self, start: Tuple[int, int], goal: Tuple[int, int]) -> Optional[List[Tuple[int, int]]]:
        pass

    @staticmethod
    def reconstruct_path(came_from: Dict[Tuple[int, int], Optional[Tuple[int, int]]], 
                         start: Tuple[int, int], 
                         goal: Tuple[int, int]) -> List[Tuple[int, int]]:
        path = []
        current = goal
        while current != start:
            path.append(current)
            current = came_from[current]
        path.append(start)
        path.reverse()
        return path

    def visualize_step(self, current: Tuple[int, int]):
        self.visualizer.make_boxes()
        self.visualizer.update_current(current)
        self.visualizer.draw_screen()
        time.sleep(0.2)

class BFSPathFinder(PathFinder):
    def find_path(self, start: Tuple[int, int], goal: Tuple[int, int]) -> Optional[List[Tuple[int, int]]]:
        if start == goal:
            return [start]

        frontier = [(start, [start])]
        reached = set([start])

        while frontier:
            current_node, path = frontier.pop(0)
            self.visualize_step(current_node)

            for next_node in self.maze.get_neighbors(current_node):
                if next_node == goal:
                    return path + [next_node]
                if next_node not in reached:
                    reached.add(next_node)
                    frontier.append((next_node, path + [next_node]))
        return None

class GBFSPathFinder(PathFinder):
    def find_path(self, start: Tuple[int, int], goal: Tuple[int, int]) -> Optional[List[Tuple[int, int]]]:
        if start == goal:
            return [start]
        
        frontier = PriorityQueue()
        frontier.put(start, 0)
        came_from: Dict[Tuple[int, int], Optional[Tuple[int, int]]] = {start: None}
        reached: Set[Tuple[int, int]] = set([start])
        
        while not frontier.empty():
            current = frontier.get()
            self.visualize_step(current)
            
            if current == goal:
                return self.reconstruct_path(came_from, start, goal)
            
            for child in self.maze.get_neighbors(current):
                if child not in reached:
                    reached.add(child)
                    came_from[child] = current
                    frontier.put(child, self.manhattan_distance(child, goal))
                    
        return None

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

    maze = Maze(maze_grid)
    visualizer = Visualizer.Visualizer()
    visualizer.set_map(maze_grid)

    start = (1, 1)
    goal = (7, 8)

    def run_pathfinder(path_finder: PathFinder):
        path = path_finder.find_path(start, goal)
        if path:
            print(f"Path found using {path_finder.__class__.__name__}:", path)
            print(f"Total moves: {len(path) - 1}")
            for node in path:
                visualizer.update_current(node)
                visualizer.draw_screen()
                time.sleep(0.2)
        else:
            print(f"No path found using {path_finder.__class__.__name__}.")

    bfs_finder = BFSPathFinder(maze, visualizer)
    gbfs_finder = GBFSPathFinder(maze, visualizer)

    print("Running BFS...")
    visualizer.set_init_func(lambda: run_pathfinder(bfs_finder))
    visualizer.draw()

    print("\nRunning GBFS...")
    visualizer.set_init_func(lambda: run_pathfinder(gbfs_finder))
    visualizer.draw()

if __name__ == "__main__":
    main()