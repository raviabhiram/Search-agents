'''
Solving the n-queens using IDS and A*
Author: Abhiram Ravi Bharadwaj
'''

import copy
from ids import ids
from a_star import a_star
from node import Node
from draw import draw_maze
import sys

'''
Function to perform the action of placing a queen.
@:param node: The current node whose next state is to be created.
@:param action: Which queen is to be placed.
'''

def action_fn(node, action):
	parent_config = node.state_config  # The current state before placing the next queen.
	child_config = copy.deepcopy(parent_config)  # A copy to update the child's config.
	child_config['current_pos'] = (parent_config['current_pos'][0] + 1, action)  # Place the queen.
	if child_config['current_pos'] not in parent_config['blocked']:  # Check if the location is valid.
		size = child_config['n']
		x = child_config['current_pos'][0]
		y = child_config['current_pos'][1]
		for i in range(size):  # Mark the positions that this queen can attack.
			child_config['blocked'].add((x, i))
			child_config['blocked'].add((i, y))
			if x - i >= 0 and y + i < size:
				child_config['blocked'].add((x - i, y + i))
			if x + i < size and y + i < size:
				child_config['blocked'].add((x + i, y + i))
			if x + i < size and y - i >= 0:
				child_config['blocked'].add((x + i, y - i))
			if x - i >= 0 and y - i >= 0:
				child_config['blocked'].add((x - i, y - i))
		return Node(child_config, node, str(action))  # Return the child node with new.
	return None

'''
Function to test if all queens are placed and none attacking any other.
@:param node: The current state which needs to satisfy the goal test.
'''

def goal_test_fn(node):
	if node.state_config['current_pos'][0] == node.state_config['n'] - 1:
		return True

def cost_fn(node, heuristic_fn):
	return 0

def heuristic(node):
	return 0

'''
Function to parse the input and create the initial state configuaration.
@:param n: The number of queens.
'''

def parse_input(n):
	actions = []  # Actions specify the current queen number to be placed.
	for i in range(n):
		actions.append(i)
	return actions, {'problem': 'n-queen', 'blocked': set([]), 'current_pos': (-1, -1), 'n': n}

'''
Function to print the board with queens placed.
@:param node: The state in which the board is.
'''

def print_board(node):
	if node:
		board = []
		for row in range(node.state_config['n']):
			board.append([])
			for col in range(node.state_config['n']):
				board[row].append('.')
		while node.state_config['current_pos'][0] >= 0:
			board[node.state_config['current_pos'][0]][node.state_config['current_pos'][1]] = 'Q'
			node = node.parent
		board_string = ''
		for line in board:
			board_string += str(line) + '\n'
		print(board_string)
		return board
	print('No solution')
	return None

def main(argv):
	if len(argv) != 2:
		print("Usage: `python3 ", argv[0], " <number_of_queens>`");
		exit(1)
	n = int(argv[1])
	actions, initial_state_config = parse_input(n)
	initial_state = Node(initial_state_config)
	# final_state_ids, nodes = ids(actions, initial_state, goal_test_fn, action_fn, n)
	final_state_as, nodes = a_star(actions, initial_state, cost_fn, action_fn, goal_test_fn, heuristic)
	board = print_board(final_state_as)
	if board:
		draw_maze(board)

if __name__ == '__main__':
	main(sys.argv)
