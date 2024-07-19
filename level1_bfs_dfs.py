def get_neighbors(current, maze):
    neighbors = []
    x, y = current
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    for dx, dy in directions:
        nx, ny = x + dx, y + dy
        if 0 <= nx < len(maze) and 0 <= ny < len(maze[0]) and maze[nx][ny] != -1:
            neighbors.append((nx, ny))
    return neighbors

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

def dfs(start, goal, maze):
    if start == goal:
        return [start]
    
    stack = [(start, [start])]  # Initialize stack (current_node, path_so_far)
    while stack:
        current_node, path = stack.pop()
        for next in get_neighbors(current_node, maze):
            if next not in path:
                if next == goal:
                    return path + [next]
                stack.append((next, path + [next]))  # Push neighbor and extended path to stack
    return [-1]

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

path = dfs(start, goal, maze)
if path:
    print("Path found:", path)
    print(f"Total moves: {len(path) - 1}")
else:
    print("No path found within the given constraints.")
