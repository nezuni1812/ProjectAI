import heapq

class PriorityQueue:
    def __init__(self):
        self.elements = []
    
    def empty(self):
        return len(self.elements) == 0
    
    def put(self, item, priority):
        heapq.heappush(self.elements, (priority, item))
    
    def get(self):
        return heapq.heappop(self.elements)[1]

def a_star_fuel(start, goal, time_limit, fuel_capacity, maze):
    frontier = PriorityQueue()
    frontier.put((start, fuel_capacity), 0)
    came_from = {}
    cost_so_far = {}
    came_from[(start, fuel_capacity)] = None
    cost_so_far[(start, fuel_capacity)] = 0
    
    while not frontier.empty():
        current_state = frontier.get()
        current, fuel = current_state
        
        if current == goal:
            return reconstruct_path_fuel(came_from, start, (current, fuel), fuel_capacity)
        
        for next, new_fuel, action in get_neighbors_with_fuel(current, fuel, fuel_capacity, maze):
            new_cost = cost_so_far[current_state] + cost_to_move(current, next, action, maze)
            new_state = (next, new_fuel)
            
            if new_cost <= time_limit and (new_state not in cost_so_far or new_cost < cost_so_far[new_state]):
                cost_so_far[new_state] = new_cost
                priority = new_cost + heuristic(next, goal, new_fuel, fuel_capacity, maze)
                frontier.put(new_state, priority)
                came_from[new_state] = (current_state, action)
    
    return None  # No path found within time and fuel constraints

def reconstruct_path_fuel(came_from, start, goal_state, fuel_capacity):
    path = []
    current_state = goal_state
    while current_state != (start, fuel_capacity):
        current, fuel = current_state
        prev_state, action = came_from[current_state]
        path.append((current, action))
        current_state = prev_state
    path.append((start, 'start'))
    path.reverse()
    return path

def get_neighbors_with_fuel(current, fuel, fuel_capacity, maze):
    neighbors = []
    for next in get_neighbors(current, maze):
        if fuel > 0:
            neighbors.append((next, fuel - 1, 'move'))
    
    if is_gas_station(current, maze) and fuel < fuel_capacity:
        neighbors.append((current, fuel_capacity, 'refuel'))
    
    return neighbors

def cost_to_move(current, next, action, maze):
    if action == 'move':
        base_cost = 1  # 1 minute to move to adjacent cell
        if is_toll_booth(next, maze):
            base_cost += toll_booth_wait_time(next, maze)
    elif action == 'refuel':
        base_cost = refuel_time(current, maze)
    return base_cost

def heuristic(node, goal, fuel, fuel_capacity, maze):
    distance = manhattan_distance(node, goal)
    return distance +  refuel_time(node, maze)

def manhattan_distance(node, goal):
    x1, y1 = node
    x2, y2 = goal
    return abs(x1 - x2) + abs(y1 - y2)

def get_neighbors(current, maze):
    neighbors = []
    x, y = current
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    for dx, dy in directions:
        nx, ny = x + dx, y + dy
        if 0 <= nx < len(maze) and 0 <= ny < len(maze[0]) and maze[nx][ny] != -1:
            neighbors.append((nx, ny))
    return neighbors

def is_toll_booth(node, maze):
    x, y = node
    return maze[x][y] > 1 and maze[x][y] < 10

def toll_booth_wait_time(node, maze):
    x, y = node
    return maze[x][y]

def is_gas_station(node, maze):
    x, y = node
    return maze[x][y] <= -2

def refuel_time(node, maze):
    x, y = node
    return abs(maze[x][y]) - 1 #F(a) = abs(a) - 1

# Example usage
maze = [
    [0, 0, 0, 0, -1, -1, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, -1, 0, -1],
    [0, 0, -1, -1, -1, 0, 0, -1, 0, -1],
    [0, 0, 0, 0, -1, 0, 0, -1, 0, 0],
    [0, 0, -1, -1, -1, 0, 0, -1, -1, 0],
    [1, 0, -1, 0, 0, 0, 0, 0, -1, 0],
    [0, 0, -2, 0, -1, 4, -1, 8, -1, 0],  # -2 represents a gas station F1
    [0, 0, 0, 0, -1, 0, 0, 0, 0, 0],
    [0, -1, -1, -1, -1, 0, 0, 0, 0, 0],
    [0, 0, 5, 0, 0, 0, -1, -1, -1, 0]
]
# -2 represents for F1, -3 represents for F2, F(a) = abs(a) - 1

start = (1, 1)  # Starting point 'S'
goal = (7, 8)  # Goal point 'G'
time_limit = 20  # Delivery time limit
fuel_capacity = 10  # Maximum fuel capacity

path = a_star_fuel(start, goal, time_limit, fuel_capacity, maze)
if path:
    print("Path found:", path)
    total_time = sum(cost_to_move(path[i][0], path[i+1][0], path[i+1][1], maze) for i in range(len(path)-1))
    print(f"Total time: {total_time} minutes")
    print(f"Total moves: {len(path) - 1}")
else:
    print("No path found within the given constraints.")
