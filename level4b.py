import heapq
import random
import numpy as np

class PriorityQueue:
    def __init__(self):
        self.elements = []

    def empty(self):
        return len(self.elements) == 0

    def put(self, item, priority):
        heapq.heappush(self.elements, (priority, item))

    def get(self):
        return heapq.heappop(self.elements)[1]

class Agent:
    def __init__(self, start, goal, fuel, time_limit, is_main=False, name=None):
        self.start = start
        self.goal = goal
        self.fuel = fuel
        self.time_limit = time_limit
        self.is_main = is_main
        self.name = name

def whca_star(agents, maze, fuel_capacity, window_size=5):
    start_state = tuple((agent.start[0], agent.start[1], agent.fuel, 0) for agent in agents)

    # Initialize reservation table
    reservation_table = {}

    paths = []
    for i, agent in enumerate(agents):
        path = single_agent_whca(agent, i, maze, fuel_capacity, window_size, reservation_table)
        if path is None:
            print(f"No path found for agent {agent.name}")
            return None
        paths.append(path)

        # Update reservation table
        for t, (_, pos, next_pos, _) in enumerate(path):
            if t not in reservation_table:
                reservation_table[t] = set()
            reservation_table[t].add(pos)
            reservation_table[t].add(next_pos)

    return merge_paths(paths)

def single_agent_whca(agent, agent_index, maze, fuel_capacity, window_size, reservation_table):
    start_state = (agent.start[0], agent.start[1], agent.fuel, 0)
    frontier = PriorityQueue()
    frontier.put(start_state, 0)
    came_from = {start_state: None}
    cost_so_far = {start_state: 0}

    best_path = None
    best_cost = float('inf')
    suboptimal_path = None
    suboptimal_cost = float('inf')

    while not frontier.empty():
        current_state = frontier.get()

        if current_state[:2] == agent.goal:
            path = reconstruct_single_path(came_from, start_state, current_state, agent, maze)
            if cost_so_far[current_state] <= agent.time_limit:
                if cost_so_far[current_state] < suboptimal_cost:
                    suboptimal_path = path
                    suboptimal_cost = cost_so_far[current_state]
                if cost_so_far[current_state] < best_cost:
                    best_path = path
                    best_cost = cost_so_far[current_state]
            elif cost_so_far[current_state] < best_cost:
                best_path = path
                best_cost = cost_so_far[current_state]

        for next_state in get_single_agent_next_states(current_state, agent, maze, fuel_capacity, reservation_table):
            new_cost = cost_so_far[current_state] + 1
            if is_toll_booth(next_state[:2], maze):
                new_cost += toll_booth_wait_time(next_state[:2], maze)
            if is_gas_station(next_state[:2], maze):
                new_cost += refuel_time(next_state[:2], maze)

            if new_cost < best_cost and (next_state not in cost_so_far or new_cost < cost_so_far[next_state]):
                cost_so_far[next_state] = new_cost
                priority = new_cost + manhattan_distance(next_state[:2], agent.goal)
                frontier.put(next_state, priority)
                came_from[next_state] = current_state

                # Update reservation table for the window
                if new_cost < window_size:
                    if new_cost not in reservation_table:
                        reservation_table[new_cost] = set()
                    reservation_table[new_cost].add(next_state[:2])

    return suboptimal_path if suboptimal_path else best_path

def single_agent_whca2(agent, agent_index, time_limit, fuel_capacity, maze, window_size, reservation_table):
    start_state = (0, 0, fuel_capacity, agent.start, []) # path_cost, current_time, current_fuel, current, path
    frontier = PriorityQueue()
    frontier.put(0 + heuristic(agent.start, agent.goal), start_state)
    
    reached = {}  # Dictionary to store the states with path cost, time, and fuel
    reached[(agent.start, 0, fuel_capacity)] = 0  # Store the initial state

    came_from = {start_state: None}

    best_path = None
    best_cost = float('inf')
    suboptimal_path = None
    suboptimal_cost = float('inf')

    while not frontier.empty():
        path_cost, current_time, current_fuel, current, path = frontier.get()
        current_state = (path_cost, current_time, current_fuel, current, path)

        path = path + [current]
        if current == agent.goal:
            # if reached[(path_cost, current_time, current_fuel)] <= agent.time_limit:
            #     if reached[current_state] < suboptimal_cost:
            #         suboptimal_path = path
            #         suboptimal_cost = reached[current_state]
            #     if reached[current_state] < best_cost:
            #         best_path = path
            #         best_cost = reached[current_state]
            # elif reached[current_state] < best_cost:
            #     best_path = path
            #     best_cost = reached[current_state]
            return path

        for next_state, new_fuel, action in get_single_agent_next_states(current_state, agent, maze, fuel_capacity, reservation_table):
            new_cost = path_cost + 1
            new_time = current_time + time_to_move(next_state, action, maze)
            if action == "move":
                new_fuel = current_fuel - 1
            elif action == "refuel":
                new_fuel = fuel_capacity
                
            state = (next_state, new_time, new_fuel)
            if new_time <= time_limit and new_fuel >= 0:
                if state not in reached or new_cost < reached[state]:
                    reached[state] = new_cost
                    priority = new_cost + heuristic(next_state, goal)
                    frontier.put(priority, (new_cost, new_time, new_fuel, next_state, path))

    return None  # No path found within time limit

def get_single_agent_next_states(state, agent, maze, fuel_capacity, reservation_table):
    path_cost, time, fuel, current, path = state
    (x, y) = current
    next_states = []

    for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0), (0, 0)]:  # (0, 0) represents waiting
        nx, ny = x + dx, y + dy
        if is_valid_move(nx, ny, maze) and not is_reserved(nx, ny, time + 1, reservation_table):
            if (dx, dy) == (0, 0):
                next_states.append((nx, ny, fuel, time + 1, maze, 'wait'))
            new_fuel = fuel - 1 if (dx, dy) != (0, 0) else fuel  # No fuel consumption when waiting
            if new_fuel >= 0:
                if is_gas_station((nx, ny), maze):
                    next_states.append((nx, ny, fuel_capacity, time + refuel_time(next, maze), maze, 'refuel'))
                else:
                    next_states.append((nx, ny, new_fuel, time + 1, 'move'))
    return next_states

def time_to_move(next, action, maze):
    if action == 'move':
        x, y = next
    elif action == 'wait':
        return 1
    elif action == 'refuel':
        return refuel_time(next, maze)
    
def is_reserved(x, y, time, reservation_table):
    return time in reservation_table and (x, y) in reservation_table[time]

def reconstruct_single_path(came_from, start, goal, agent, maze):
    path = []
    current = goal
    while current != start:
        path.append(current)
        current = came_from[current]
    path.append(start)
    path.reverse()

    processed_path = []
    for i in range(len(path) - 1):
        current_pos = path[i][:2]
        next_pos = path[i + 1][:2]

        if current_pos == next_pos:
            action = "wait"
        elif is_gas_station(next_pos, maze):
            action = "refuel"
        elif is_toll_booth(next_pos, maze):
            action = "toll"
        else:
            action = "move"

        processed_path.append((agent.name, current_pos, next_pos, action))

    return processed_path

def merge_paths(paths):
    max_length = max(len(path) for path in paths)
    merged_path = []
    for i in range(max_length):
        for path in paths:
            if i < len(path):
                merged_path.append(path[i])
    return merged_path

def is_valid_move(x, y, maze):
    return 0 <= x < len(maze) and 0 <= y < len(maze[0]) and maze[x][y] != -1

def is_at_toll_booth(node, maze, time):
    if()
def is_toll_booth(node, maze):
    x, y = node
    return maze[x][y] > 1 and maze[x][y] < 10

def toll_booth_wait_time(node, maze):
    x, y = node
    return maze[x][y] + 1

def is_gas_station(node, maze):
    x, y = node
    return maze[x][y] <= -2

def refuel_time(node, maze):
    x, y = node
    return abs(maze[x][y]) # F(a) = abs(a) - 1

def manhattan_distance(pos1, pos2):
    return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])

def heuristic(node, goal):
    return manhattan_distance(node, goal)

def calculate_path_time(path, maze):
    total_time = 0
    for step in path:
        _, current_pos, next_pos, action = step
        if action == "move" or action == "wait":
            total_time += 1
        elif action == "refuel":
            total_time += refuel_time(next_pos, maze)
        elif action == "toll":
            total_time += toll_booth_wait_time(next_pos, maze)
    return total_time


def get_agent_stop(path, agents, maze):
    updated_path = []
    stopped_agents = set()
    
    for step in path:
        agent_name, current_pos, next_pos, action = step
        agent = next(a for a in agents if a.name == agent_name)
        
        if agent_name not in stopped_agents:
            agent_path = [s for s in path if s[0] == agent_name]
            total_time = calculate_path_time(agent_path, maze)
            
            if total_time > agent.time_limit:
                stopped_agents.add(agent_name)
                # Add a "wait" action at the current position for the remaining time
                remaining_time = agent.time_limit - calculate_path_time(updated_path, maze)
                for _ in range(remaining_time):
                    updated_path.append((agent_name, current_pos, current_pos, "wait"))
            else:
                updated_path.append(step)
        
    return updated_path

def generate_new_subagent_and_recreate_path(path, agents, maze, fuel_capacity):
    result_path = []
    while True:
        new_path_segment = []

        for step in path:
            result_path.append(step)
            agent_name, old_position, current_position, action = step
            if action == "createnewgoal":
                continue
            # Determine the index of the agent
            if len(agent_name) > 1:
                index_agent = int(agent_name[1:])
                agents[index_agent].start = current_position
            else:
                index_agent = 0
                agents[0].start = current_position

            if agent_name == 'S' and current_position == agents[0].goal:
                print("Main agent S has reached the goal.")
                return result_path

            if agent_name != 'S' and current_position == agents[index_agent].goal:
                print(f"Sub-agent {agent_name} has reached the goal.")
                new_position = generate_new_position(maze)
                result_path.append((agent_name, current_position, new_position, "createnewgoal"))
                print(new_position)
                if new_position:
                    agents[index_agent].start = current_position
                    agents[index_agent].goal = new_position

                    print(f"New goal for {agent_name}: {new_position}")
                    new_path_segment = whca_star(agents, maze, fuel_capacity)
                    if new_path_segment is None:
                        print("No path found for at least one agent.")
                        return result_path
                    else:
                        # Prepare to continue with the new path segment
                        path = new_path_segment
                        break
        
        # If no new path segment was generated, break the loop
        if not new_path_segment:
            break

        # Continue the outer loop with the new path segment
        path = new_path_segment

    return result_path

# Hàm lấy vị trí hiện tại của các agent 
def take_current_positions_of_agent(path, num_agents):
    latest_positions = {}
    for action in reversed(path):
        if len(latest_positions) == num_agents:
            break
        
        agent_name = action[0]
        current_pos = action[2] 
        
        if agent_name not in latest_positions:
            latest_positions[agent_name] = current_pos
    return latest_positions

def generate_new_position(maze):
    # Tạo danh sách các ô trống không có giá trị -1 
    empty_squares = [(x, y) for x in range(len(maze)) for y in range(len(maze[0])) if maze[x][y] != -1]
    
    if not empty_squares:
        return None
    
    return random.choice(empty_squares)
