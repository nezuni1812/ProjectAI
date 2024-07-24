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

    class Node:
        def __init__(self, position, g_cost, h_cost, parent=None):
            self.position = position
            self.g_cost = g_cost
            self.h_cost = h_cost
            self.f_cost = self.g_cost + self.h_cost
            self.parent = parent
        def __lt__(self, other):
            return self.f_cost < other.f_cost

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

    # Functions for level 2
    @staticmethod
    def cost_to_move(current, next, maze):
        base_cost = 1 # 1 min to move to adjacent cell
        if PathFinderLevel2.is_toll_booth(next, maze):
            base_cost += PathFinderLevel2.toll_booth_wait_time(next, maze)
        return base_cost
    @staticmethod
    def is_toll_booth(node, maze):
        x, y = node
        return maze[x][y] > 1
    @staticmethod
    def toll_booth_wait_time(node, maze):
        x, y = node
        return maze[x][y]

    @abstractmethod
    def find_path(self, start: Tuple[int, int], goal: Tuple[int, int]) -> Optional[List[Tuple[int, int]]]:
        pass

# Level 1

class BFSPathFinder(PathFinder):
    def find_path(self, start: Tuple[int, int], goal: Tuple[int, int]) -> Optional[List[Tuple[int, int]]]:
        if start == goal:
            return [start]

        frontier = [(start, [start])]
        reached = set([start])

        while frontier:
            current, path = frontier.pop(0)
            print('Checking:', current)
            self.visualize_step(current)

            for next_node in self.get_neighbors(current, self.maze):
                if next_node == goal:
                    return path + [next_node]
                if next_node not in reached:
                    reached.add(next_node)
                    frontier.append((next_node, path + [next_node]))
        return None
    
class DFSPathFinder(PathFinder):
    def find_path(self, start: Tuple[int], goal: Tuple[int]) -> List[Tuple[int]] | None:
        if start == goal:
            return [start]
        stack = [(start, [start])]
        while stack:
            current, path = stack.pop()
            print('Checking: ', current)
            self.visualize_step(current)

            for next in self.get_neighbors(current, self.maze):
                if next not in path:
                    if next == goal:
                        return path + [next]
                    stack.append((next, path + [next]))
        return None
    
class UCSPathFinder(PathFinder):
    def find_path(self, start: Tuple[int, int], goal: Tuple[int, int]) -> Optional[List[Tuple[int, int]]]:
        visited = set()
        frontier = PriorityQueue()
        frontier.put(start, 0)
        came_from = {start: None}
        cost_so_far = {start: 0}

        while not frontier.empty():
            current = frontier.get()
            print('Checking: ', current)
            self.visualize_step(current)

            if current == goal:
                return self.reconstruct_path(came_from, start, goal)

            visited.add(current)

            for neighbor in self.get_neighbors(current, self.maze):
                new_cost = cost_so_far[current] + 1  # Assuming each step costs 1
                if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
                    cost_so_far[neighbor] = new_cost
                    priority = new_cost
                    frontier.put(neighbor, priority)
                    came_from[neighbor] = current

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
            print('Checking: ', current)
            self.visualize_step(current)
            
            if current == goal:
                return self.reconstruct_path(came_from, start, goal)
            
            for child in self.get_neighbors(current, self.maze):
                if child not in reached:
                    reached.add(child)
                    came_from[child] = current
                    frontier.put(child, self.heuristic(child, goal)) 
        return None
class AStarPathFinder(PathFinder):
    def find_path(self, start: Tuple[int], goal: Tuple[int]) -> List[Tuple[int]] | None:
        start_node = self.Node(start, 0, self.heuristic(start, goal))
        frontier = PriorityQueue()
        frontier.put(start_node, start_node.f_cost)
        came_from = {start: None}
        reached = {start: 0}
        while not frontier.empty():
            current = frontier.get()
            print('Checking: ', current.position)
            self.visualize_step(current.position)

            if current.position == goal:
                return self.reconstruct_path(came_from, start, goal)

            for neighbor in self.get_neighbors(current.position, self.maze):
                new_cost = reached[current.position] + 1

                if neighbor not in reached or new_cost < reached[neighbor]:
                    reached[neighbor] = new_cost
                    priority = new_cost + self.heuristic(neighbor, goal)
                    neighbor_node = self.Node(neighbor, new_cost, self.heuristic(neighbor, goal), current)
                    frontier.put(neighbor_node, priority)
                    came_from[neighbor] = current.position
        return None


# Implement A* algorithm for level 2    
class PathFinderLevel2(PathFinder):
    def find_path(self, start: Tuple[int], goal: Tuple[int]) -> Optional[List[Tuple[int]]]:
        start_node = self.Node(start, 0, self.heuristic(start, goal))
        frontier = PriorityQueue()
        frontier.put(start_node, start_node.f_cost)
        came_from = {start: None}
        reached = {start: 0}
        
        while not frontier.empty():
            current = frontier.get()
            print('Checking: ', current.position)
            self.visualize_step(current.position)

            if current.position == goal:  # Compare current.position with goal
                return self.reconstruct_path(came_from, start, goal)

            for neighbor in self.get_neighbors(current.position, self.maze):
                new_cost = reached[current.position] + self.cost_to_move(current.position, neighbor, self.maze)

                if neighbor not in reached or new_cost < reached[neighbor]:
                    reached[neighbor] = new_cost
                    priority = new_cost + self.heuristic(neighbor, goal)
                    neighbor_node = self.Node(neighbor, new_cost, self.heuristic(neighbor, goal), current)
                    frontier.put(neighbor_node, priority)
                    came_from[neighbor] = current.position

        return None