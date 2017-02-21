# Artificial Intelligence Nanodegree
## Introductory Project: Diagonal Sudoku Solver

# Question 1 (Naked Twins)
Q: How do we use constraint propagation to solve the naked twins problem?  
A: The naked twins is a constraint when two boxes in the same unit holds same two numbers, the peer boxes in the unit cannot have this two numbers. The algorithm for naked twins problem is as follows
	Step1: Iterate all the units in the sudoko board
	Step2: for each unit, identify all possible naked twins.
	Step3: remove the digits in naked twins from its peers in the unit.
		e.g. Below is an example of an unit before and after apllying naked twins.
		Value of column unit3 before: {A3:4, B3:6, C3:8, D3:2379, E3:379, F3:23, G3:1, H3:5, I3:23}
		Value of column unit3 after : {A3:4, B3:6, C3:8, D3:79, E3:79, F3:23, G3:1, H3:5, I3:23}	

# Question 2 (Diagonal Sudoku)
Q: How do we use constraint propagation to solve the diagonal sudoku problem?  
A: The diagonal sudoku problem can be solved by adding two more units that represents the two major diagonal of the sudoku board. The techniques elimination, only choice and naked twins are applied to the diagonal units until the problem is solved or stalled.

### Install

This project requires **Python 3**.

We recommend students install [Anaconda](https://www.continuum.io/downloads), a pre-packaged Python distribution that contains all of the necessary libraries and software for this project. 
Please try using the environment we provided in the Anaconda lesson of the Nanodegree.

##### Optional: Pygame

Optionally, you can also install pygame if you want to see your visualization. If you've followed our instructions for setting up our conda environment, you should be all set.

If not, please see how to download pygame [here](http://www.pygame.org/download.shtml).

### Code

* `solutions.py` - You'll fill this in as part of your solution.
* `solution_test.py` - Do not modify this. You can test your solution by running `python solution_test.py`.
* `PySudoku.py` - Do not modify this. This is code for visualizing your solution.
* `visualize.py` - Do not modify this. This is code for visualizing your solution.

### Visualizing

To visualize your solution, please only assign values to the values_dict using the ```assign_values``` function provided in solution.py

### Data

The data consists of a text file of diagonal sudokus for you to solve.