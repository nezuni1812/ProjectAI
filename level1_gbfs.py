import heapq

def get_neighbors(current, maze):
    neighbors = []
    x, y = current
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    for dx, dy in directions:
        nx, ny = x + dx, y + dy
        if 0 <= nx < len(maze) and 0 <= ny < len(maze[0]) and maze[nx][ny] != -1:
            neighbors.append((nx, ny))
    return neighbors
    
def heuristic(node, goal):
    return manhattan_distance(node, goal)

def manhattan_distance(node, goal):
    x1, y1 = node
    x2, y2 = goal
    return abs(x1 - x2) + abs(y1 - y2)

class PriorityQueue:
    def __init__(self):
        self.elements = []
    
    def empty(self):
        return len(self.elements) == 0
    
    def put(self, item, priority):
        heapq.heappush(self.elements, (priority, item))
    
    def get(self):
        return heapq.heappop(self.elements)[1]

def bfs(start, goal, maze):
    if start == goal:
        return [start]

    frontier = ([(start, [start])])  # Initialize queue (current_node, path_so_far)
    reached = set([start])  # Initialize visited set
    while frontier:
        current_node, path = frontier.pop(0)
        for next in get_neighbors(current_node, maze):
            if next == goal:
                return path + [next]

            if next not in reached:
                reached.add(next)
                frontier.append((next, path + [next]))  # Enqueue neighbor and extended path
    return [-1]

def gbfs(start, goal, maze):
    if start == goal:
        return [start]
        
    frontier = PriorityQueue()
    frontier.put(start, 0)
    came_from = {}
    came_from[start] = None
    reached = set([start])
    
    while not frontier.empty():
        current = frontier.get()
        
        if current == goal:
            return reconstruct_path(came_from, start, goal)
        
        for child in get_neighbors(current, maze):
            if child not in reached:
                reached.add(child)
                came_from[child] = current
                frontier.put(child, heuristic(child, goal))
                
    return None

def reconstruct_path(came_from, start, goal):
    path = []
    current = goal
    while current != start:
        path.append(current)
        current = came_from[current]
    path.append(start)
    path.reverse()
    return path

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

path = gbfs(start, goal, maze)
if path:
    print("Path found:", path)
    print(f"Total moves: {len(path) - 1}")
else:
    print("No path found within the given constraints.")
