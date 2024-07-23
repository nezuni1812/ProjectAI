import heapq

class Node:
    def __init__(self, position, g_cost, h_cost, parent=None):
        self.position = position
        self.g_cost = g_cost
        self.h_cost = h_cost
        self.f_cost = g_cost + h_cost
        self.parent = parent

    def __lt__(self, other):
        return self.f_cost < other.f_cost

def manhattan_distance(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def get_neighbors(position, maze):
    x, y = position
    neighbors = []
    for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:  # Right, Down, Left, Up
        new_x, new_y = x + dx, y + dy
        if 0 <= new_x < len(maze) and 0 <= new_y < len(maze[0]) and maze[new_x][new_y] != -1:
            neighbors.append((new_x, new_y))
    return neighbors

def a_star(start, goal, maze):
    start_node = Node(start, 0, manhattan_distance(start, goal))
    open_list = [start_node]
    closed_set = set()

    while open_list:
        current_node = heapq.heappop(open_list)

        if current_node.position == goal:
            path = []
            while current_node:
                path.append(current_node.position)
                current_node = current_node.parent
            return path[::-1]  # Return reversed path

        closed_set.add(current_node.position)

        for neighbor_pos in get_neighbors(current_node.position, maze):
            if neighbor_pos in closed_set:
                continue

            neighbor = Node(
                neighbor_pos,
                current_node.g_cost + 1,
                manhattan_distance(neighbor_pos, goal),
                current_node
            )

            if neighbor not in open_list:
                heapq.heappush(open_list, neighbor)
            else:
                # If this path to neighbor is better, update the neighbor
                idx = open_list.index(neighbor)
                if open_list[idx].g_cost > neighbor.g_cost:
                    open_list[idx] = neighbor
                    heapq.heapify(open_list)

    return None  # No path found

# Example usage
maze = [
    [0, 0, 0, 0, -1, -1, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, -1, 0, -1],
    [0, 0, -1, -1, -1, 0, 0, -1, 0, -1],
    [0, 0, 0, 0, -1, 0, 0, -1, 0, 0],
    [0, 0, -1, -1, -1, 0, 0, -1, -1, 0],
    [1, 0, -1, 0, 0, 0, 0, 0, -1, 0],
    [0, 0, 0, 0, -1, 4, -1, 8, -1, 0],
    [0, 0, 0, 0, -1, 0, 0, 0, 0, 0],
    [0, -1, -1, -1, -1, 0, 0, 0, 0, 0],
    [0, 0, 5, 0, 0, 0, -1, -1, -1, 0]
]

start = (1, 1)  # Starting point 'S'
goal = (7, 8)  # Goal point 'G'

path = a_star(start, goal, maze)

if path:
    print("Path found:")
    for step in path:
        print(step)
else:
    print("No path found.")

# Visualization of the path in the maze
def print_maze_with_path(maze, path):
    for i, row in enumerate(maze):
        for j, cell in enumerate(row):
            if (i, j) in path:
                print("* ", end="")
            elif cell == -1:
                print("# ", end="")
            else:
                print(". ", end="")
        print()

print("\nMaze with path:")
print_maze_with_path(maze, path)
