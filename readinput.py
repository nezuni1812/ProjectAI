def read_input_file(file_path):
    with open(file_path, 'r') as file:
        first_line = file.readline().strip()
        n, m, t, f = map(int, first_line.split()) #Number of rows, columns, delivery time, fuel tank 

        maze = [] # Maze structure      
        positions = {} # Dictionary to hold positions of Start, Goal and Fuel
        for i in range(n):
            line = file.readline().strip().split()
            maze.append(line)
            for j, value in enumerate(line):
                if value.startswith('S') or value.startswith('G') or value.startswith('F'):
                    positions[value] = (i, j)

    return n, m, t, f, maze, positions

file_path = 'input.txt'
n, m, t, f, maze, positions = read_input_file(file_path)
print(f'n: {n}, m: {m}, t: {t}, f: {f}')
print('Maze:')
print(maze)
# for line in maze:
#     print(' '.join(line))
print('Positions:', positions)