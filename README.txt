# Project 1 - Search: Delivery System
This repository contains our code for the group homework of the class Introduction to Artificial Intelligence.

The inputs, path search algorithms, the main UI code along with class diagrams of some of our custom classes are included.

Source code: [GitHub](https://github.com/nezuni1812/Searching-Algorithms-for-Delivery-System)

# Demo video
[![Video](https://img.youtube.com/vi/o3kB2hNbsmE/maxresdefault.jpg)](https://youtu.be/o3kB2hNbsmE)


# Running the UI
All of our code are written in Python so a system with a relatively modern version of Python (>= 3.10) and PIP are required to run the program.

## Installing dependencies
```bash
pip install -r requirements.txt
```
## Running the UI
```bash
python main.py
```
A Tkinter window will pop up and show the welcome screen, noticing the user that they can choose which level to run using the number keys. More information are available inside each level.

When a level is has completed, the user can switch to another level by pressing the number key corresponding to the level index, i.e. `1`, `2`, `3` or `4`. To restart a level, the user can press the `enter` key.


# Changing level's inputs
Each level has 5 test cases, or inputs. Their file names are: 

`input1_level1.txt` \
`input2_level1.txt` \
...\
`input5_level4.txt`


## Level 1, 2 and 3
```python
level_list.append(lambda *args: level_1(visualizer, 'input5_level1.txt'))
level_list.append(lambda *args: level_2(visualizer, 'input5_level2.txt'))
level_list.append(lambda *args: level_3_UI_implementation.level_3(visualizer, 'input5_level3.txt'))
```
User can directly edit the input file name in the `main.py` file by their level. For level 1, all the path searching implementations will use the same input maze.

## Level 4
For level 4, user can change the input by clicking the dropdown and choosing which file to take data from.


# Class diagram
The `PathFinder.py` and `Visualizer.py` contains our classes for the project.

Each path search algorithm in level 1 and 2 are implemented using an abstract base class with common methods like `get_neighbors`, `reconstruct_path`, `heuristic`..., custom Priority Queue data structure and a pure virtual function `find_path` that is implemented by its sub classes.

The UML diagram are written in Markdown file with Mermaid code, which can be previewed on [Mermaid Live editor](https://mermaid.live/) or using a VSCode extension like [Markdown Preview Mermaid Support](https://marketplace.visualstudio.com/items?itemName=bierner.markdown-mermaid).