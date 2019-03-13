'''
Author: Abhiram Ravi Bharadwaj
'''

import copy
import sys
import time
import random
import math
from ids import ids
from a_star import a_star
from node import Node
from draw import draw_maze

'''
Function to perform the various actions from a given maze state.
@:param parent: The current state from which the action is to be performed.
@:param action: The action to be performed on the node passed.
'''

def action_fn(parent, action):
	current_config = parent.state_config  # Get the parent's configuration of the maze.
	child_config = copy.deepcopy(current_config)  # Will eventually be modified for each child to store the state.
	# child_config = current_config
	child_config['nodes'] += 1
	child = None
	current_x = current_config['current_pos'][0]
	current_y = current_config['current_pos'][1]
	if action == 'up':
		if current_x > 0 and str((current_x - 1, current_y)) not in current_config['blocked']:
			child_config['blocked'][str((current_x - 1, current_y))] = True
			child_config['current_pos'] = (current_x - 1, current_y)
			child_config['cost'] = current_config['cost'] + 1
			child = Node(child_config, parent, 'up')
	elif action == 'left':
		if current_y > 0 and str((current_x, current_y - 1)) not in current_config['blocked']:
			child_config['blocked'][str((current_x, current_y - 1))] = True
			child_config['current_pos'] = (current_x, current_y - 1)
			child_config['cost'] = current_config['cost'] + 1
			child = Node(child_config, parent, 'left')
	elif action == 'down':
		if current_x < current_config['height'] - 1 and str((current_x + 1, current_y)) not in current_config['blocked']:
			child_config['blocked'][str((current_x + 1, current_y))] = True
			child_config['current_pos'] = (current_x + 1, current_y)
			child_config['cost'] = current_config['cost'] + 1
			child = Node(child_config, parent, 'down')
	elif action == 'right':
		if current_y < current_config['length'] - 1 and str((current_x, current_y + 1)) not in current_config['blocked']:
			child_config['blocked'][str((current_x, current_y + 1))] = True
			child_config['current_pos'] = (current_x, current_y + 1)
			child_config['cost'] = current_config['cost'] + 1
			child = Node(child_config, parent, 'right')
	return child

'''
Function to test if the node passed has reached the end of the maze.
@:param node: The node which needs to be tested.
'''

def goal_test_fn(node):
	if node.state_config['current_pos'] == node.state_config['destination']:
		return True
	return False

'''
Function to return the cost of a particular node. Cost is the sum of current cost and heuristic.
@:param node: The node whose cost is to be returned.
'''
def cost_fn(node, heuristic_fn):
	x1 = node.state_config['current_pos'][0]
	y1 = node.state_config['current_pos'][1]
	x2 = node.state_config['destination'][0]
	y2 = node.state_config['destination'][1]
	return (node.state_config['cost'] + heuristic_fn(x1, y1, x2, y2))

def heuristic_zero(x1, y1, x2, y2):
	return 0

def heuristic_rand(x1, y1, x2, y2):
	return random.randint(0, 10000)

def heuristic_manhattan(x1, y1, x2, y2):
	return abs(x2 - x1) + abs(y2 - y1)

def heuristic_straight_line(x1, y1, x2, y2):
	return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)

'''
Function to read a file and return the data.
@:param file_name: The file which needs to be read.
'''

def read_file(file_name):
	with open(file_name, 'r') as file:  # Open file in read mode.
		data = file.read().splitlines()
	maze = []
	for line in data:
		maze.append(line.split())
	return maze

'''
Function to parse the input read.
'''

def parse_input(data):
	blocked = {
		'(0, 0)': True
	}  # The list of nodes that cannot be accessed. In this case rocks or visited nodes.
	length = len(data[0])
	height = len(data)
	for i in range(height):
		for j in range(length):
			if data[i][j] == '1':
				blocked[str((i, j))] = True
	return {'problem': 'maze', 'blocked': blocked, 'height': height, 'length': length, 'current_pos': (0, 0),
	        'destination': (height - 1, length - 1), 'nodes': 0, 'cost': 0}

'''
Function to convert the final state into a visual maze and return the string to be printed.
@:param node: The final node from which the entire path can be traced back.
@:param initial_config: The starting configuration of the maze.
'''

def print_maze(node, initial_config):
	result = []  # Variable to store the final maze in.
	step_count = 0
	for i in range(initial_config['height']):
		result.append([])
		for j in range(initial_config['length']):
			result[i].append('.')
	for key in initial_config['blocked']:
		loc = key.replace('(', '').replace(')', '').split(',')
		result[int(loc[0])][int(loc[1])] = '1'
	while node is not None:
		step_count += 1
		result[node.state_config['current_pos'][0]][node.state_config['current_pos'][1]] = 'X'
		node = node.parent
	return_string = ''
	for line in result:
		return_string += str(line) + '\n'
	return result, return_string, step_count

'''
Function to print the result of the search algorithm.
'''

def print_result(algo, time, final_state, nodes, initial_state_config):
	if final_state is None:
		print(algo, '\t\t--------No solution.-------')
		return None
	else:
		maze, maze_string, step_count = print_maze(final_state, initial_state_config)
		# print('End state:\n', maze_string)
		b = math.exp((math.log(nodes)) / step_count)
		print(algo, '\t\t', time, '\t\t', nodes, '\t\t', step_count, '\t\t', b)
		return maze

'''
Main function to run the search algorithms from.
'''

def maze_solver(args):
	actions = ['right', 'down', 'left', 'up']
	heuristics = [heuristic_rand, heuristic_zero, heuristic_manhattan, heuristic_straight_line]
	data = read_file(args[1])  # The maze question file which is passed as first argument.
	initial_state_config = parse_input(data)
	initial_state = Node(initial_state_config)
	maze = None
	print('Algo\t|\tTime\t|\tNodes\t|\tSteps\t|\tBranching Factor')
	for heuristic in heuristics:
		initial_node = copy.deepcopy(initial_state)
		start = time.time()
		final_state_as, nodes = a_star(actions, initial_node, cost_fn, action_fn, goal_test_fn, heuristic)
		end = time.time()
		maze = print_result('A* with ' + heuristic.__name__, end - start, final_state_as, nodes, initial_state_config)
	# start = time.time()
	# final_state_ids, nodes = ids(actions, initial_state_config['length'] + initial_state_config['height'], initial_state,
	#                              goal_test_fn, action_fn)
	# end = time.time()
	# maze = print_result('IDS', end - start, final_state_ids, nodes, initial_state_config)
	# if maze:
	# 	draw_maze(maze)

if __name__ == '__main__':
	maze_solver(sys.argv)
