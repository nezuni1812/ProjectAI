import Visualizer
import level4

if __name__ == '__main__':
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

    starts = [(1, 1),
(8, 5),
(2, 5)]
    goals = [(7, 8),
(4, 6),
(9, 0)]
    
    agents = [
        level4.Agent(starts[0], goals[0], 10, time_limit=20, is_main=True, name="S"),
        level4.Agent(starts[1], goals[1], 10, time_limit=20, name="S1"),
        level4.Agent(starts[2], goals[2], 10, time_limit=10, name="S2"),
    ]

    fuel_capacity = 10

    # Find the path using WHCA*
    path = level4.whca_star(agents, maze, fuel_capacity)
    path = level4.get_agent_stop(path, agents, maze)
    visuals =  Visualizer.Visualizer()
    
    visuals.set_map(maze)
    
    for i, point in enumerate(starts):
        visuals.add_point(point, 'S' if i == 0 else 'S' + str(i))
        
    for i, point in enumerate(goals):
        visuals.add_point(point, 'G' if i == 0 else 'G' + str(i))
        
    visuals.make_boxes()
    
    # print(visuals.maze)
    # visuals.root.mainloop()
    
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

        # Plot the maze and paths
        # level4.plot_maze(maze, path, agents)
        visuals.draw_path_turn_based(path)
        
        # visuals.root.mainloop()
    else:
        print("No path found for at least one agent.")