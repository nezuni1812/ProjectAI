def read_input_file(file_path):
    with open(file_path, 'r') as file:
        first_line = file.readline().strip()
        n, m, t, f = map(int, first_line.split())  # Number of rows, columns, delivery time, fuel tank 

        maze = []  # Maze structure      
        positions = {}  # Dictionary to hold positions of Start, Goal, and Fuel
        for i in range(n):
            line = file.readline().strip().split()
            row = []
            for j, value in enumerate(line):
                if value.startswith('S') or value.startswith('G'):
                    row.append(0)
                    positions[value] = (i, j)
                elif value.startswith('F'):
                    num = int(value[1:])  # Extract the numeric part after 'F'
                    row.append(-1 - num)  # Convert F1 to -2, F2 to -3, etc.
                    positions[value] = (i, j)
                else:
                    row.append(int(value))  # Convert numeric values to integers
            maze.append(row)

    return n, m, t, f, maze, positions

# file_path = 'input.txt'
# n, m, t, f, maze, positions = read_input_file(file_path)
# print(f'n: {n}, m: {m}, t: {t}, f: {f}')
# print('Maze:')
# print(maze)
# # for line in maze:
# #     print(' '.join(line))
# print('Positions:', positions)