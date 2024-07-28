import Visualizer
import level4
import ReadInput

def level_4(visuals, file_path):
    n, m, time_limit, fuel_capacity, raw_maze, maze, starts, goals = ReadInput.read_input_file(file_path)

    visuals.canvas.delete('all')

    agents = []
    for i, (start, goal) in enumerate(zip(starts, goals)):
        if i == 0:
            # The first agent is the main agent
            agents.append(level4.Agent(start, goal, fuel_capacity, time_limit, is_main=True, name="S"))
        else:
            # Other agents
            agents.append(level4.Agent(start, goal, fuel_capacity, time_limit, name=f"S{i}"))

    # Find the path using WHCA*
    try:
        path = level4.whca_star(agents, maze, fuel_capacity)
        path = level4.get_agent_stop(path, agents, maze)
        path = level4.generate_new_subagent_and_recreate_path(path, agents, maze, fuel_capacity)
    except:
        print("No path found for at least one agent.")
        path = None

    visuals.set_map(raw_maze)
    visuals.make_boxes()
    
    if path:
        print("Paths found:")
        print(path)
        for agent in agents:
            agent_path = [step for step in path if step[0] == agent.name]
            total_time = level4.calculate_path_time(agent_path, maze)
            print(f"Agent {agent.name}:")
            print(f"  Path: {agent_path}")
            print(f"  Total time: {total_time}")
            print(f"  Within time limit: {'Yes' if total_time <= agent.time_limit else 'No'}")

        visuals.draw_path_turn_based(path)
    else:
        lef_padding = len(maze[0]) * 50 + 20
        visuals.canvas.create_text(lef_padding, 12, text='Level 4: Multi agents', font=('Cascadia Code', 14, 'bold'), anchor='nw')
        visuals.canvas.create_text(lef_padding, 40, text='Step', font=('Cascadia Code', 14), anchor='nw')
        visuals.canvas.create_text(lef_padding, 120, text='<Arrow ▶> for next move\n<Space ␣> for autoplay', font=('Cascadia Code', 14), anchor='nw')

        visuals.canvas.create_text(lef_padding, 180, text='No path found :<', font=('Cascadia Code', 14), anchor='nw', fill='red')
        print("No path found for at least one agent.")
        
if __name__ == '__main__':
    visuals = Visualizer.Visualizer()
    level_4(visuals, 'input2_level4.txt')