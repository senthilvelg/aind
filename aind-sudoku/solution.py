# Solution of Udacity AIND Project 1 Sudoku Puzzle.
# Solution by Senthil. Most functions and code are reused from the lessons.
# Note To reviewers: Please suggest ways to improve the code for naked_twins function.

# Global values for initializing the board for a 9x9 sudoku board
assignments = []
values = []
rows = 'ABCDEFGHI'
cols = '123456789'


# Cross product of elements in A and elements in B.
def cross(a, b):
    return [s + t for s in a for t in b]


row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in ('ABC', 'DEF', 'GHI') for cs in ('123', '456', '789')]
diagonal_units = [['A1', 'B2', 'C3', 'D4', 'E5', 'F6', 'G7', 'H8', 'I9'],
                  ['A9', 'B8', 'C7', 'D6', 'E5', 'F4', 'G3', 'H2', 'I1']]
unitlist = row_units + column_units + square_units + diagonal_units
boxes = cross(rows, cols)
units_dict = dict((s, [u for u in unitlist if s in u]) for s in boxes)
peers_dict = dict((s, set(sum(units_dict[s], [])) - {s}) for s in boxes)


def assign_value(values, box, value):
    """
    Assigns a value to a given box. If it updates the board record it.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}
        box(string): box name. e.g. A2
        value: value of a box. e.g. '1234'
    """
    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values


def naked_twins(values):
    """
    Eliminate values using the naked twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """

    # Iterate each unit and identify all boxes that has the values with length of 2. Then identify
    # twin pairs within this group. An unit can have multiple naked twins. for each of the naked twin,
    # remove the digits present in twins from all the peers that belongs to the unit.
    for unit in unitlist:
        twin_dict = {}
        for box in unit:
            box_val = values[box]
            if len(box_val) is 2:
                if box_val in twin_dict:
                    twin_dict[box_val].append(box)
                else:
                    twin_dict[box_val] = [box]

        for key in twin_dict:
            if len(twin_dict[key]) is 2:
                peers = set(unit) - set(twin_dict[key])
                for digit in values[twin_dict[key][0]]:
                    for peer in peers:
                        values[peer] = values[peer].replace(digit, '')
    return values


def grid_values(grid):
    """
    Creates a dictionary with box name as key and the possible value of the box as value.
    Args:
        grid (string):
    """
    assert len(grid) == 81, "Input string length must be 81 chars long. (9x9)"
    items = []
    for item in grid:
        if item == '.':
            items.append('123456789')
        else:
            items.append(item)
    return dict(zip(boxes, items))


def display(values):
    """
    Display the values as a 2-D grid.
    Input: The sudoku in dictionary form
    Output: None

    Args:
        values(dict):
    """
    width = 1 + max(len(values[s]) for s in boxes)
    line = '+'.join(['-' * (width * 3)] * 3)
    for r in rows:
        print(''.join(values[r + c].center(width) + ('|' if c in '36' else '')
                      for c in cols))
        if r in 'CF': print(line)
    return


def eliminate(values):
    """
    Eliminates number from boxes based on solved values from its peers.
    Args:
        values(dict):

    Returns:
        values after applying the elimination stratergy.
    """
    solved_boxes = [box for box in boxes if len(values[box]) == 1]
    for sbox in solved_boxes:
        digit = values[sbox]
        for peer in peers_dict[sbox]:
            values[peer] = values[peer].replace(digit, '')
    return values


def only_choices(values):
    """
    Applies the only choice technique based on the values of its peer.
    Args:
        values()dict:

    Returns:

    """
    for unit in unitlist:
        for digit in '123456789':
            positions = [box for box in unit if digit in values[box]]
            if len(positions) == 1:
                values[positions[0]] = digit
    return values


def reduce_puzzle(values):
    """
    Applies elimination, only choice and naked twins techniqies to the board and returns the final result
    if the board is solved or False if its stalled and requires solving by search.
    Args:
        values(dict):

    Returns:

    """
    stalled = False
    while not stalled:
        # Check how many boxes have a determined value
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])

        # Apply Eliminate Strategy
        values = eliminate(values)

        # Apply Only Choice Strategy
        values = only_choices(values)

        # Apply naked twins Stratergy
        values = naked_twins(values)

        # Check how many boxes have a determined value, to compare
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])

        # If no new values were added, stop the loop.
        stalled = solved_values_before == solved_values_after

        # Sanity check, return False if there is a box with zero available values:
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values


def search(values):
    "Using depth-first search and propagation, create a search tree and solve the sudoku."
    # First, reduce the puzzle using the previous function
    values = reduce_puzzle(values)

    if values is False:
        return False  # Stalled

    if all(len(values[s]) == 1 for s in boxes):
        return values

    # Choose one of the unfilled squares with the fewest possibilities
    n, s = min((len(values[s]), s) for s in boxes if len(values[s]) > 1)

    # Now use recursion to solve each one of the resulting sudokus, and if one returns a value (not False), return that answer!
    for value in values[s]:
        new_values = values.copy()
        new_values[s] = value
        result = search(new_values)
        if result:
            return result


def solve(grid):
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.
    """
    values = grid_values(grid)
    return search(values)


if __name__ == '__main__':

    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    values = grid_values(diag_sudoku_grid)
    display(values)
    display(solve(diag_sudoku_grid))

    try:
        from visualize import visualize_assignments

        visualize_assignments(assignments)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
