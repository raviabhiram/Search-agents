'''
Macro that can be used to perform iterative deepening search.
Author: Abhiram Ravi Bharadwaj
'''

import copy

NO_FRONTIER = False
NODES = 0

'''
Function to create child nodes of the current node and check if any of them satisfy the goal test.
@:param node: The node whose children are to be created.
@:param actions: The list of possible actions that can be taken.
@:param goal_test_fn: The goal test for each problem that tells us to stop looking for solution.
@:param action_fn: The function that sets the state for the child node.
@:param check_flag: Solution is always found only at leaf nodes. We perform goal test only for leaf nodes.
'''

def check_children(node, actions, goal_test_fn, action_fn, check_flag):
	global NO_FRONTIER
	global NODES
	for action in actions:
		child_node = action_fn(node, action)  # Create new nodes for children.
		if child_node is not None:
			NODES += 1
			if check_flag and goal_test_fn(child_node):
				return True, child_node
			else:
				node.children.append(child_node)
		if check_flag and child_node:
			NO_FRONTIER &= False
	return False, None

'''
Recursive function to perform ids until a certain depth is reached or a solution is reached.  
@:param actions: The list of possible actions that can be taken.
@:param nodes: The nodes whose children are to be created.
@:param goal_test_fn: The goal test for each problem that tells us to stop looking for solution.
@:param action_fn: The function that sets the state for the child node.
@:param depth: The total depth to which this iteration of ids must go to.
@:param current_depth: The current depth to which ids has reached.
'''

def perform_ids(actions, nodes, goal_test_fn, action_fn, depth, current_depth):
	global NO_FRONTIER
	if current_depth >= depth:  # If the depth is breached, no solution has been found.
		NO_FRONTIER &= False
		return False, None
	for node in nodes:  # Create children nodes for each node in this level.
		solution_found, solution_node = check_children(node, actions, goal_test_fn, action_fn, current_depth + 1 == depth)
		if solution_found:
			return solution_found, solution_node
	for node in nodes:
		if len(node.children) > 0:
			solution_found, solution_node = perform_ids(actions, node.children, goal_test_fn, action_fn, depth,
			                                            current_depth + 1)
		if solution_found:
			return solution_found, solution_node
	return False, None

'''
Function to iteratively perform search until a solution is found.
@:param actions: The list of possible actions that can be taken.
@:param initial_node: The initial problem node from which to branch and find solutions.
@:param goal_test_fn: The goal test for each problem that tells us to stop looking for solution.
@:param action_fn: The function that sets the state for the child node.
@:param start_depth: The depth at which search for solutions should start.
'''

def ids(actions, initial_node, goal_test_fn, action_fn, start_depth=0):
	global NO_FRONTIER
	global NODES
	if goal_test_fn(initial_node):
		return initial_node
	depth = start_depth
	solution_found = False
	solution_node = None
	while solution_found == False and NO_FRONTIER == False:
		NO_FRONTIER = True
		NODES = 0
		# print('Checking at depth: ', depth)
		root_node = copy.deepcopy(initial_node)
		solution_found, solution_node = perform_ids(actions, [root_node], goal_test_fn, action_fn, depth, 0)
		depth += 1
	return solution_node, NODES