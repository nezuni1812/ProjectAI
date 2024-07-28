import Visualizer
import level3
import ReadInput

def level_3(visualizer, file_path):
    n, m, time_limit, fuel_capacity, raw_maze, maze, starts, goals = ReadInput.read_input_file(file_path)

    visualizer.root.unbind('<Return')
    visualizer.root.bind("<Return>", lambda *args: level_3(visualizer, file_path))

    start = starts[0]  # Starting point 'S'
    goal = goals[0]  # Goal point 'G'
    path = level3.a_star_fuel(start, goal, time_limit, fuel_capacity, maze)
    visualizer.set_map(raw_maze)
    visualizer.make_boxes()
    
    if path:
        print("Path found:", path)
        total_cost = sum(level3.cost_to_move() for i in range(len(path)-1))
        print(f"Total cost: {total_cost}")
        
        lef_padding = len(maze[0]) * 50 + 20
        visualizer.canvas.create_text(lef_padding, 12, text='Level 3: fuel limitation', font=('Cascadia Code', 14, 'bold'), anchor='nw')
        visualizer.canvas.create_text(lef_padding, 40, text='Modified A* with fuel limitation: ' + str(fuel_capacity), font=('Cascadia Code', 14), anchor='nw')
        visualizer.canvas.create_text(lef_padding, 68, text='Success. Total cost: ' + str(len(path) - 1), font=('Cascadia Code', 14), anchor='nw', fill='green')
        visualizer.canvas.create_text(lef_padding, 100, text='<Enter ⏎> to start the algorithm', font=('Cascadia Code', 14), anchor='nw')
        visualizer.make_boxes()
        visualizer.draw_screen()

        for node in path:
            visualizer.canvas.delete('all')
            visualizer.canvas.create_text(lef_padding, 12, text='Level 3: fuel limitation', font=('Cascadia Code', 14, 'bold'), anchor='nw')
            visualizer.canvas.create_text(lef_padding, 40, text='Modified A* with fuel limitation: ' + str(fuel_capacity), font=('Cascadia Code', 14), anchor='nw')
            visualizer.canvas.create_text(lef_padding, 68, text='Success. Total cost: ' + str(len(path) - 1), font=('Cascadia Code', 14), anchor='nw', fill='green')
            visualizer.canvas.create_text(lef_padding, 100, text='<Enter ⏎> to start the algorithm', font=('Cascadia Code', 14), anchor='nw')

            visualizer.make_boxes()
            visualizer.update_current(node)
            visualizer.draw_screen()
            visualizer.root.after(50)
            
        visualizer.root.mainloop()
    else:
        lef_padding = len(maze[0]) * 50 + 20
        visualizer.canvas.create_text(lef_padding, 12, text='Level 3: fuel limitation', font=('Cascadia Code', 14, 'bold'), anchor='nw')
        visualizer.canvas.create_text(lef_padding, 40, text='Modified A* with fuel limitation: ' + str(fuel_capacity), font=('Cascadia Code', 14), anchor='nw')
        visualizer.canvas.create_text(lef_padding, 68, text='No path found :<', font=('Cascadia Code', 14), anchor='nw', fill='red')
        visualizer.draw_screen()

        print("No path found within the given constraints.")
        visualizer.root.mainloop()
        
if __name__ == '__main__':
    visualizer = Visualizer.Visualizer()
    level_3(visualizer, 'input3_level3.txt')