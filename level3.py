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

def a_star_fuel(start, goal, time_limit, fuel_capacity, maze):
    frontier = PriorityQueue()
    frontier.put(0, (0, start, [], 0, fuel_capacity))  # (priority, (path_cost, current position, path, current_fuel, current_time))
    
    while not frontier.empty():
        path_cost, current, path, current_time, current_fuel = frontier.get()
        path = path + [current]
        
        if current == goal and current_time <= time_limit and current_fuel >= 0:
            return path  
        
        for next, new_fuel, action in get_neighbors_with_fuel(current, current_fuel, fuel_capacity, maze):
            new_cost = path_cost + cost_to_move()
            new_time = current_time + time_to_move(next, action, maze)
            if action == "move":
                new_fuel = current_fuel - cost_to_move()
            elif action == "refuel":
                new_fuel = fuel_capacity

            if new_time <= time_limit and new_fuel >= 0:
                priority = new_cost + heuristic(next, goal)
                frontier.put(priority, (new_cost, next, path, new_time, new_fuel))
    
    return None  # No path found within time limit

def get_neighbors_with_fuel(current, fuel, fuel_capacity, maze):
    neighbors = []
    for next in get_neighbors(current, maze):
        if is_gas_station(next, maze):
            neighbors.append((next, fuel_capacity, 'refuel'))
        else:
            neighbors.append((next, fuel - 1, 'move'))

    return neighbors

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
    return 1  # Each move costs 1 fuel unit

def time_to_move(next, action, maze):
    if action == 'move':
        x, y = next
        if maze[x][y] > 0:
            return maze[x][y] + 1
        elif maze[x][y] == 0:
            return 1
    elif action == 'refuel':
        return refuel_time(next, maze)
    
def heuristic(node, goal):
    return manhattan_distance(node, goal)

def manhattan_distance(node, goal):
    x1, y1 = node
    x2, y2 = goal
    return abs(x1 - x2) + abs(y1 - y2)

def is_gas_station(node, maze):
    x, y = node
    return maze[x][y] <= -2

def refuel_time(node, maze):
    x, y = node
    return abs(maze[x][y]) - 1

file_path = 'input1_level3.txt'
n, m, time_limit, fuel_capacity, maze, positions = ReadInput.read_input_file(file_path)

start = positions['S']  # Starting point 'S'
goal = positions['G']  # Goal point 'G'

path = a_star_fuel(start, goal, time_limit, fuel_capacity, maze)
if path:
    print("Path found:", path)
    total_cost = sum(cost_to_move() for i in range(len(path)-1))
    print(f"Total cost: {total_cost}")
else:
    print("No path found within the given constraints.")
