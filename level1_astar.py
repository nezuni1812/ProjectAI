import heapq
import ReadInput

class PriorityQueue:
    def __init__(self):
        self.elements = []
    
    def empty(self):
        return len(self.elements) == 0
    
    def put(self, priority, item):
        heapq.heappush(self.elements, (priority, item))
    
    def get(self):
        return heapq.heappop(self.elements)[1]

def a_star(start, goal, maze):
    frontier = PriorityQueue()
    frontier.put(0, (0, start, []))  # (priority, (path cost, current position, path))
    
    while not frontier.empty():
        path_cost, current, path = frontier.get()
        path = path + [current]
        
        if current == goal:
            return path  
        
        for next in get_neighbors(current, maze):
            new_cost = path_cost + cost_to_move()
            if next not in path or new_cost < path_cost:
                priority = new_cost + heuristic(next, goal)
                frontier.put(priority, (new_cost, next, path))
    
    return None  

def get_neighbors(current, maze):
    neighbors = []
    x, y = current
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    for dx, dy in directions:
        nx, ny = x + dx, y + dy
        if 0 <= nx < len(maze) and 0 <= ny < len(maze[0]) and maze[nx][ny] != -1:
            neighbors.append((nx, ny))
    return neighbors

def cost_to_move():
    return 1

def heuristic(node, goal):
    return manhattan_distance(node, goal)

def manhattan_distance(node, goal):
    x1, y1 = node
    x2, y2 = goal
    return abs(x1 - x2) + abs(y1 - y2)

file_path = 'input1_level1.txt'
n, m, time_limit, fuel_capacity, maze, positions = ReadInput.read_input_file(file_path)

start = positions['S']  # Starting point 'S'
goal = positions['G']  # Goal point 'G'

path = a_star(start, goal, time_limit, maze)
if path:
    print("Path found:", path)
    total_cost = sum(cost_to_move() for i in range(len(path)-1))
    print(f"Total cost: {total_cost}")
else:
    print("No path found within the given constraints.")