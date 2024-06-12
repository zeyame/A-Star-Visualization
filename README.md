# A* Pathfinding Visualization

This project is a visualization of the A* pathfinding algorithm using Pygame. The A* algorithm is widely used in pathfinding and graph traversal, and it is often used in many fields of computer science due to its performance and accuracy.

## Description

This visualization tool allows users to interactively set start and end points on a grid, place barriers, and watch the A* algorithm find the shortest path between the start and end points.

## Features

- Interactive grid where users can place start, end, and barrier nodes.
- Visual representation of the A* algorithm's process.
- Ability to reset the grid and re-run the algorithm with different configurations.

## Installation

To run this project locally, you'll need to have Python installed. Follow these steps:

1. Clone the repository:

    ```bash
    git clone https://github.com/zeyame/A-Star-Visualization.git
    cd A-Star-Visualization
    ```

2. Install the required dependencies:

    ```bash
    pip install pygame
    ```

3. Run the application:

    ```bash
    python main.py
    ```

## Usage

Once the application is running, you can interact with the grid to set up your pathfinding scenario.

## Controls

- **Left Click**: 
  - First click sets the start node.
  - Second click sets the end node.
  - Subsequent clicks set barrier nodes.

- **Right Click**: 
  - Removes the node (start, end, or barrier) at the clicked position.

- **Space Bar**: 
  - Starts the A* algorithm visualization.

- **C Key**: 
  - Clears the grid.

## Acknowledgements
This project was developed as a learning exercise to understand and visualize the A* pathfinding algorithm. Special thanks to the Pygame community for providing an excellent library for game development in Python.
