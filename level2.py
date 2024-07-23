import heapq
import ReadInput

class PriorityQueue:
    def __init__(self):
        self.elements = []
    
    def empty(self):
        return len(self.elements) == 0
    
    def put(self, item, priority):
        heapq.heappush(self.elements, (priority, item))
    
    def get(self):
        return heapq.heappop(self.elements)[1]

def a_star(start, goal, time_limit, maze):
    frontier = PriorityQueue()
    frontier.put(start, 0)
    came_from = {}
    cost_so_far = {}
    came_from[start] = None
    cost_so_far[start] = 0
    
    while not frontier.empty():
        current = frontier.get()
        
        if current == goal and cost_so_far[current] <= time_limit:
            return reconstruct_path(came_from, start, goal)
        
        for next in get_neighbors(current, maze):
            new_cost = cost_so_far[current] + cost_to_move(current, next, maze)
            if new_cost <= time_limit and (next not in cost_so_far or new_cost < cost_so_far[next]):
                cost_so_far[next] = new_cost
                priority = new_cost + heuristic(next, goal)
                frontier.put(next, priority)
                came_from[next] = current
    
    return None  # No path found within time limit

def reconstruct_path(came_from, start, goal):
    path = []
    current = goal
    while current != start:
        path.append(current)
        current = came_from[current]
    path.append(start)
    path.reverse()
    return path

def get_neighbors(current, maze):
    neighbors = []
    x, y = current
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    for dx, dy in directions:
        nx, ny = x + dx, y + dy
        if 0 <= nx < len(maze) and 0 <= ny < len(maze[0]) and maze[nx][ny] != -1:
            neighbors.append((nx, ny))
    return neighbors

def cost_to_move(current, next, maze):
    base_cost = 1  # 1 minute to move to adjacent cell
    if is_toll_booth(next, maze):
        base_cost += toll_booth_wait_time(next, maze)
    return base_cost

def is_toll_booth(node, maze):
    x, y = node
    return maze[x][y] > 1

def toll_booth_wait_time(node, maze):
    x, y = node
    return maze[x][y]

def heuristic(node, goal):
    return manhattan_distance(node, goal)

def manhattan_distance(node, goal):
    x1, y1 = node
    x2, y2 = goal
    return abs(x1 - x2) + abs(y1 - y2)

file_path = 'input1_level2.txt'
n, m, time_limit, fuel_capacity, maze, positions = ReadInput.read_input_file(file_path)

start = positions['S']  # Starting point 'S'
goal = positions['G']  # Goal point 'G'


path = a_star(start, goal, time_limit, maze)
print("Path found:", path)
