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

class PathFinder(ABC):
    def __init__(self, maze: list, visualizer: Visualizer.Visualizer):
        self.maze = maze
        self.visualizer = visualizer
        self.visualizer.set_map(maze)

    @staticmethod
    def heuristic(node: Tuple[int, int], goal: Tuple[int, int]) -> int:
        return abs(node[0] - goal[0]) + abs(node[1] - goal[1])
    
    @staticmethod
    def get_neighbors(current: Tuple[int, int], maze):
        neighbors = []
        x, y = current
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < len(maze) and 0 <= ny < len(maze[0]) and maze[nx][ny] != -1:
                neighbors.append((nx, ny))
        return neighbors
    
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

    def start_visualizer(self, start: Tuple[int, int], goal: Tuple[int, int], map: list = None):
        if map is not None:
            self.maze = map
            self.visualizer.set_map(map)
            
        path = self.find_path(start, goal)
        
        if path:
            print("Path found:", path)
            print(f"Total moves: {len(path) - 1}")
            for node in path:
                self.visualizer.update_current(node)
                self.visualizer.draw_screen()
                time.sleep(.2)
        
        else:
            print("No path found.")
        
        pass

    def visualize_step(self, current: Tuple[int, int]):
        self.visualizer.make_boxes()
        self.visualizer.update_current(current)
        self.visualizer.draw_screen()
        time.sleep(0.1)

    @abstractmethod
    def find_path(self, start: Tuple[int, int], goal: Tuple[int, int]) -> Optional[List[Tuple[int, int]]]:
        pass


class BFSPathFinder(PathFinder):
    def find_path(self, start: Tuple[int, int], goal: Tuple[int, int]) -> Optional[List[Tuple[int, int]]]:
        if start == goal:
            return [start]

        frontier = [(start, [start])]
        reached = set([start])

        while frontier:
            current_node, path = frontier.pop(0)
            print('Checking:', current_node)
            self.visualize_step(current_node)

            for next_node in self.get_neighbors(current_node, self.maze):
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
            
            for child in self.get_neighbors(current, self.maze):
                if child not in reached:
                    reached.add(child)
                    came_from[child] = current
                    frontier.put(child, self.heuristic(child, goal))
                    
        return None
