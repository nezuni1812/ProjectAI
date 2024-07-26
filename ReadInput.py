def read_input_file(file_path):
    with open(file_path, 'r') as file:
        first_line = file.readline().strip()
        n, m, t, f = map(int, first_line.split())  # Number of rows, columns, delivery time, fuel tank 

        raw_maze = []
        maze = []
        start = [None] * 10  # Initialize with None, assuming max 10 start points
        goal = [None] * 10   # Initialize with None, assuming max 10 goal points
        for i in range(n):
            line = file.readline().strip().split()
            raw_row = line.copy()  # Copy the original row for raw maze
            processed_row = []
            for j, value in enumerate(line):
                if value.startswith('S'):
                    processed_row.append(0)
                    if value == 'S':
                        start[0] = (i, j)
                    else:
                        index = int(value[1:])
                        start[index] = (i, j)
                elif value.startswith('G'):
                    processed_row.append(0)
                    if value == 'G':
                        goal[0] = (i, j)
                    else:
                        index = int(value[1:])
                        goal[index] = (i, j)
                elif value.startswith('F'):
                    num = int(value[1:])  # Extract the number after 'F'
                    processed_row.append(-1 - num)  # Convert F1 to -2, F2 to -3, etc.
                else:
                    processed_row.append(int(value))  # Convert numeric values to integers
            raw_maze.append(raw_row)
            maze.append(processed_row)
            
    # Remove any None values at the end of the lists
    start = [pos for pos in start if pos is not None]
    goal = [pos for pos in goal if pos is not None]

    return n, m, t, f, raw_maze, maze, start, goal

# file_path = 'input2_level4.txt'
# n, m, t, f, raw_maze, maze, start, goal = read_input_file(file_path)
# print(f'n: {n}, m: {m}, t: {t}, f: {f}')
# print('Maze:')
# for i, row in enumerate(maze):
#     print(f'{i:2d}: {" ".join(map(str, row))}')
# print('Starts:', start)
# print('Goals:', goal)