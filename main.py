import numpy as np
import heapq
import time


class Node():

    def __init__(self, parent=None, state=None):
        self.parent = parent
        self.state = state

        self.g = 0
        self.h = 0
        self.f = 0

    def __lt__(self, other):
        return self.f < other.f


def swapPositions(arr, pos1, pos2):
    new_arr = arr.copy()
    new_arr[pos1], new_arr[pos2] = new_arr[pos2], new_arr[pos1]
    return new_arr


def step_right(state, blank_space, column):
    new_state = state
    if blank_space % column < column - 1:
        new_state = swapPositions(new_state, blank_space, blank_space + 1)
        return new_state
    else:
        return None


def step_left(state, blank_space, column):
    new_state = state.copy()
    if blank_space % column > 0:
        new_state = swapPositions(new_state, blank_space, blank_space - 1)
        return new_state
    else:
        return None


def step_up(state, blank_space, column):
    new_state = state.copy()
    if blank_space - column >= 0:
        new_state = swapPositions(new_state, blank_space, blank_space - column)
        return new_state
    else:
        return None


def step_down(state, blank_space, row, column):
    new_state = state.copy()
    if blank_space + column < row * column:
        new_state = swapPositions(new_state, blank_space, blank_space + column)
        return new_state
    else:
        return None


# generates every possible neighbor of current state
def generate_children(state, rows, cols):
    children = []
    blank_space = state.index(0)
    child1 = step_right(state, blank_space, cols)
    if child1 is not None:
        children.append(child1)
    child2 = step_left(state, blank_space, cols)
    if child2 is not None:
        children.append(child2)
    child3 = step_up(state, blank_space, cols)
    if child3 is not None:
        children.append(child3)
    child4 = step_down(state, blank_space, rows, cols)
    if child4 is not None:
        children.append(child4)

    return children


def astar(puzzle, goal, m, n, heuristic):
    start_node = Node(None, puzzle)
    start_node.h = start_node.f = start_node.g = 0
    open_list = []
    closed_list = {}
    heapq.heappush(open_list, (0, start_node))

    while len(open_list) != 0:

        # removes node with min priority from priority queue
        current_node = heapq.heappop(open_list)[1]
        current_state = current_node.state.copy()
        closed_list[tuple(current_state)] = current_node

        # if we reach the end return path
        if current_state == goal:
            path = []
            count = 0
            while current_node:
                path.append(current_node.state)
                current_node = current_node.parent
                count = count + 1
            print('Total nodes:', len(closed_list))
            print('Total steps:', count - 1)
            return path[::-1]

        children = generate_children(current_state, m, n)

        for item in children:

            cost = current_node.g + 1

            sign1 = closed_list.get(tuple(item), False)

            # if state is not in closed list
            if not sign1:
                new_node = Node(current_node, item)
                new_node.g = cost
                if heuristic == 1:
                    new_node.h = manhattan(item, goal, m, n)
                elif heuristic == 2:
                    new_node.h = misplaced_tiles(item, goal, m, n)

                new_node.f = new_node.g + new_node.h
                heapq.heappush(open_list, (new_node.f, new_node))

    print('solution does not exist')
    exit()


# calculate Manhattan distance cost between each digit of current state and the goal state
def manhattan(puzzle, goal, rows, cols):
    count = 0
    for j in range(0, rows * cols):
        for k in range(0, rows * cols):
            if puzzle[j] == goal[k] and puzzle[j] != 0:
                count += (abs((j % cols) - (k % cols)) + abs((j // cols) - (k // cols)))
    return count


# will calculate the number of misplaced tiles in the current state as compared to the goal state
def misplaced_tiles(puzzle, goal, rows, cols):
    count = 0
    for i in range(0, rows * cols):
        if puzzle[i] != goal[i] and puzzle[i] != 0:
            count = count + 1
    return count


def print_solution(arr, rows, cols):
    for state in arr:
        for i in range(len(state)):
            print(state[i], end='')
            if ((i + 1) % cols) == 0:
                print()
        print()


def main():

    # User input for initial state
    rows = int(input('Enter number of rows '))
    cols = int(input('Enter number of columns '))
    puzzle = []
    print("Enter start state ")
    for i in range(0, rows * cols):
        x = int(input())
        puzzle.append(x)

    # User input for goal state
    goal = []
    print("Enter goal state ")
    for i in range(0, rows * cols):
        x = int(input())
        goal.append(x)

    n = int(input("Enter 1 for manhattan heuristic / 2 for misplaced tiles "))
    start_time = time.time()
    solution = astar(puzzle, goal, rows, cols, n)
    print("Search time: ", (time.time() - start_time))
    print_solution(solution, rows, cols)


if __name__ == "__main__":
    main()
