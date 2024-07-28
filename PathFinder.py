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
    
    def put(self, priority, item):
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
        self.time_limit = 0

    def set_time_limit(self, time_limit):
        self.time_limit = time_limit

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
                time.sleep(.1)
        
        else:
            print("No path found.")
        

    def visualize_step(self, current: Tuple[int, int] = None, headline = None, lvl_name = None, result = None, more_text = None):
        self.visualizer.canvas.delete('all')
        self.visualizer.make_boxes()
        lef_padding = len(self.maze[0]) * 50 + 20
        if lvl_name is not None:
            self.visualizer.canvas.create_text(lef_padding, 12, text=lvl_name, font=('Cascadia Code', 14, 'bold'), anchor='nw')
        if headline is not None:
            self.visualizer.canvas.create_text(lef_padding, 40, text=headline, font=('Cascadia Code', 14), anchor='nw')
        if result is not None:
            self.visualizer.canvas.create_text(lef_padding, 68, text=result[0], font=('Cascadia Code', 14), anchor='nw', fill=result[1])
        if more_text is not None:
            self.visualizer.canvas.create_text(lef_padding, 100, text=more_text, font=('Cascadia Code', 14), anchor='nw')
        if current is not None:
            self.visualizer.update_current(current)
        self.visualizer.draw_screen()
        self.visualizer.root.after(50)

    # Functions for level 2: Time limitation
    @staticmethod
    # def cost_to_move(current, next, maze):
    def cost_to_move():
        base_cost = 1 # 1 min to move to adjacent cell
        # if PathFinderLevel2.is_toll_booth(next, maze):
        #     base_cost += PathFinderLevel2.toll_booth_wait_time(next, maze)
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

# Level 1: Basic

class BFSPathFinder(PathFinder):
    def find_path(self, start: Tuple[int, int], goal: Tuple[int, int]) -> Optional[List[Tuple[int, int]]]:
        if start == goal:
            self.visualize_step(headline='Breadth first Search', lvl_name='Level 1: Basic', result=('Success. Total cost: 1', 'green'), more_text='<Arrow ◀ ▶> to change algorithm\n<Enter ⏎> to start the algorithm')
            return [start]

        frontier = [(start, [start])]
        reached = set([start])

        while frontier:
            current, path = frontier.pop(0)
            # self.visualizer.canvas.create_text(690, 12, text='Algorithm: Breadth first Search', font=('Cascadia Code', 14))
            self.visualize_step(current, 'Breadth first Search', 'Level 1: Basic', more_text='<Arrow ◀ ▶> to change algorithm\n<Enter ⏎> to start the algorithm')
            # self.visualizer.root.after(400)

            for next_node in self.get_neighbors(current, self.maze):
                if next_node == goal:
                    path = path + [next_node]
                    self.visualize_step(headline='Breadth first Search', lvl_name='Level 1: Basic', result=('Success. Total cost: ' + str(len(path) - 1), 'green'), more_text='<Arrow ◀ ▶> to change algorithm\n<Enter ⏎> to start the algorithm')
                    return path
                if next_node not in reached:
                    reached.add(next_node)
                    frontier.append((next_node, path + [next_node]))
        
        self.visualize_step(headline='Breadth first Search', lvl_name='Level 1: Basic', result=('No path found :<', 'red'), more_text='<Arrow ◀ ▶> to change algorithm\n<Enter ⏎> to start the algorithm')
        return None
    
    
class DFSPathFinder(PathFinder):
    def find_path(self, start: Tuple[int], goal: Tuple[int]) -> List[Tuple[int]] | None:
        if start == goal:
            self.visualize_step(headline='Depth-first Search', lvl_name='Level 1: Basic', result=('Success. Total cost: 1', 'green'), more_text='<Arrow ◀ ▶> to change algorithm\n<Enter ⏎> to start the algorithm')
            return [start]
        
        stack = [(start, [start])]
        visited = set()
        visited.add(start)
        
        while stack:
            current, path = stack.pop()
            self.visualize_step(current, 'Depth-first Search', 'Level 1: Basic', more_text='<Arrow ◀ ▶> to change algorithm\n<Enter ⏎> to start the algorithm')

            for next in self.get_neighbors(current, self.maze):
                if next not in visited:
                    if next == goal:
                        path = path + [next]
                        self.visualize_step(headline='Depth-first Search', lvl_name='Level 1: Basic', result=('Success. Total cost: ' + str(len(path) - 1), 'green'), more_text='<Arrow ◀ ▶> to change algorithm\n<Enter ⏎> to start the algorithm')
                        return path
                    stack.append((next, path + [next]))
                    visited.add(next)
        
        self.visualize_step(headline='Depth-first Search', lvl_name='Level 1: Basic', result=('No path found :<', 'red'), more_text='<Arrow ◀ ▶> to change algorithm\n<Enter ⏎> to start the algorithm')
        return None
class UCSPathFinder(PathFinder):
    def find_path(self, start: Tuple[int, int], goal: Tuple[int, int]) -> Optional[List[Tuple[int, int]]]:
        visited = set()
        frontier = PriorityQueue()
        frontier.put(0, start)  # Note the order: (priority, item)
        came_from = {start: None}
        cost_so_far = {start: 0}

        while not frontier.empty():
            current = frontier.get()
            
            self.visualize_step(current, 'Uniform-cost Search', 'Level 1: Basic', more_text='<Arrow ◀ ▶> to change algorithm\n<Enter ⏎> to start the algorithm')

            if current == goal:
                path = self.reconstruct_path(came_from, start, goal)
                self.visualize_step(headline='Uniform-cost Search', lvl_name='Level 1: Basic', result=('Success. Total cost: ' + str(len(path) - 1), 'green'), more_text='<Arrow ◀ ▶> to change algorithm\n<Enter ⏎> to start the algorithm')
                return path

            visited.add(current)

            for neighbor in self.get_neighbors(current, self.maze):
                new_cost = cost_so_far[current] + 1  # Assuming each step costs 1
                if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
                    cost_so_far[neighbor] = new_cost
                    priority = new_cost
                    frontier.put(priority, neighbor)
                    came_from[neighbor] = current

        self.visualize_step(headline='Uniform-cost Search', lvl_name='Level 1: Basic', result=('No path found :<', 'red'), more_text='<Arrow ◀ ▶> to change algorithm\n<Enter ⏎> to start the algorithm')
        return None

    

class GBFSPathFinder(PathFinder):
    def find_path(self, start: Tuple[int, int], goal: Tuple[int, int]) -> Optional[List[Tuple[int, int]]]:
        if start == goal:
            self.visualize_step(headline='Greedy best first Search', lvl_name='Level 1: Basic', result=('Success. Total cost: 1', 'green'), more_text='<Arrow ◀ ▶> to change algorithm\n<Enter ⏎> to start the algorithm')
            return [start]
        
        frontier = PriorityQueue()
        frontier.put(0, start)
        came_from: Dict[Tuple[int, int], Optional[Tuple[int, int]]] = {start: None}
        reached: Set[Tuple[int, int]] = set([start])
        
        while not frontier.empty():
            current = frontier.get()
            
            self.visualize_step(current, 'Greedy best first Search', 'Level 1: Basic', more_text='<Arrow ◀ ▶> to change algorithm\n<Enter ⏎> to start the algorithm')
            
            if current == goal:
                path = self.reconstruct_path(came_from, start, goal)
                self.visualize_step(headline='Greedy best first Search', lvl_name='Level 1: Basic', result=('Success. Total cost: ' + str(len(path) - 1), 'green'), more_text='<Arrow ◀ ▶> to change algorithm\n<Enter ⏎> to start the algorithm')
                return path
            
            for child in self.get_neighbors(current, self.maze):
                if child not in reached:
                    reached.add(child)
                    came_from[child] = current
                    frontier.put(self.heuristic(child, goal), child) 
                    
        self.visualize_step(headline='Greedy best first Search', lvl_name='Level 1: Basic', result=('No path found :<', 'red'), more_text='<Arrow ◀ ▶> to change algorithm\n<Enter ⏎> to start the algorithm')
        return None
        
class AStarPathFinder(PathFinder):
    def find_path(self, start: Tuple[int], goal: Tuple[int]) -> List[Tuple[int]] | None:
        frontier = PriorityQueue()
        frontier.put(0, (0, start, []))  # (priority, (path cost, current position, path))
        reached = {}
        reached[start] = 0
        
        while not frontier.empty():
            path_cost, current, path = frontier.get()
            path = path + [current]
            self.visualize_step(current, 'A* Search', 'Level 1: Basic')
            
            if current == goal:
                self.visualize_step(headline='A* Search', lvl_name='Level 1: Basic', result=('Success. Total cost: ' + str(len(path) - 1), 'green'), more_text='<Arrow ◀ ▶> to change algorithm\n<Enter ⏎> to start the algorithm')
                return path  
            
            for next in self.get_neighbors(current, self.maze):
                new_cost = path_cost + self.cost_to_move()
                if next not in reached or new_cost < reached[next]:
                    reached[next] = new_cost
                    priority = new_cost + self.heuristic(next, goal)
                    frontier.put(priority, (new_cost, next, path))
        
        self.visualize_step(headline='A* Search', lvl_name='Level 1: Basic', result=('No path found :<', 'red'), more_text='<Arrow ◀ ▶> to change algorithm\n<Enter ⏎> to start the algorithm')
        return None  

# Implement A* algorithm for level 2: Time limitation    
class PathFinderLevel2(PathFinder):
    def wait_time(self, node, maze):
        x, y = node
        return maze[x][y]

    def find_path(self, start: Tuple[int], goal: Tuple[int]) -> Optional[List[Tuple[int]]]:
        frontier = PriorityQueue()
        frontier.put(0 + self.heuristic(start, goal), (0, 0, start, []))  # (priority, (path cost, current_time, current position, path))
        reached = {}  # Dictionary to store the states with start position, time
        reached[(start, 0)] = 0  # The value of the key is the path cost of that state(positions, time)
        
        self.visualize_step(headline='A* Search with time limit of ' + str(self.time_limit), lvl_name='Level 2: Time limitation')
        self.visualizer.root.after(600)
        
        while not frontier.empty():
            path_cost, current_time, current, path = frontier.get()
            path = path + [current]
            # Uncomment the line below for expanded node animation
            # self.visualize_step(current)
            # print('Check:', current)
            
            if current == goal:
                return path  
            
            for next in self.get_neighbors(current, self.maze):
                new_cost = path_cost + self.cost_to_move()
                new_time = current_time + self.cost_to_move() + self.wait_time(next, self.maze)
                
                state = (next, new_time)
                if new_time <= self.time_limit and (state not in reached or new_cost < reached[state]):
                    reached[state] = new_cost
                    priority = new_cost + self.heuristic(next, goal)
                    frontier.put(priority, (new_cost, new_time, next, path))
        
        self.visualize_step(headline='A* Search with time limit of ' + str(self.time_limit), lvl_name='Level 2: Time limitation', result=('No path found :<', 'red'))
        return None  # No path found within time limit