def read_input_file(file_path):
    with open(file_path, 'r') as file:
        first_line = file.readline().strip()
        n, m, t, f = map(int, first_line.split())  # Number of rows, columns, delivery time, fuel tank 

        raw_maze = []
        maze = []
        positions = {}  # Dictionary to hold positions of Start, Goal, and Fuel
        for i in range(n):
            line = file.readline().strip().split()
            raw_row = line.copy()  # Copy the original row for raw maze
            processed_row = []
            for j, value in enumerate(line):
                if value.startswith('S') or value.startswith('G'):
                    processed_row.append(0)
                    positions[value] = (i, j)
                elif value.startswith('F'):
                    num = int(value[1:])  # Extract the number after 'F'
                    processed_row.append(-1 - num)  # Convert F1 to -2, F2 to -3, etc.
                    positions[value] = (i, j)
                else:
                    processed_row.append(int(value))  # Convert numeric values to integers
            raw_maze.append(raw_row)
            maze.append(processed_row)

    return n, m, t, f, raw_maze, maze, positions

# file_path = 'input.txt'
# n, m, t, f, maze, positions = read_input_file(file_path)
# print(f'n: {n}, m: {m}, t: {t}, f: {f}')
# print('Maze:')
# for i, row in enumerate(maze):
#     print(f'{i:2d}: {" ".join(map(str, row))}')
# print('Positions:', positions)