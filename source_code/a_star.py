'''
Macro that can be plugged in to solve A* to find a solution.
Author: Abhiram Ravi Bharadwaj
'''

import heapq

NODES = 0  # Global variable to keep track of number of nodes explored.

'''
Function to create children for the chosen node.
@:param node: The node whose children are to be created.
@:param actions: The list of possible actions with which children can be created.
@:param action_fn: The function that sets the state for the child node.
@:param queue: The queue of prospective paths to explore.
'''

def create_children(node, actions, action_fn, cost_fn, heuristic_fn, queue):
	global NODES
	for action in actions:  # Create a child node for each action.
		child_node = action_fn(node, action)
		if child_node is not None:  # Add child node to the queue of unique prospects.
			NODES += 1
			heapq.heappush(queue, (cost_fn(child_node, heuristic_fn), child_node))
	return queue

'''
Function to choose the best prospect based on the cost function.
@:param queue: The queue of prospective paths to explore.
@:param visited: A queue of all nodes that have been visited already.
@:param update_fn: The function called to update the cost of all nodes once a node is selected.
'''

def choose_node(queue, visited):
	next_node = heapq.heappop(queue)[1]
	next_loc = str(next_node.state_config['current_pos']) + str(next_node.parent.state_config['current_pos'])
	while next_loc in visited:  # Find a node in the queue that has not been visited already.
		next_node = heapq.heappop(queue)[1]
		next_loc = str(next_node.state_config['current_pos']) + str(next_node.parent.state_config['current_pos'])
	visited[next_loc] = True  # Mark the node as visited.
	return next_node, queue, visited

'''
Recursive function to perform A*.
@:param actions: The list of possible actions that can be taken.
@:param node: The node from which to branch and find solutions.
@:param queue: The queue of prospective paths to explore.
@:param action_fn: The function that sets the state for the child node.
@:param goal_test_fn: The goal test for each problem that tells us to stop looking for solution.
@:param visited: A queue of all nodes that have been visited already.
'''

def perform_a_star(actions, node, cost_fn, action_fn, goal_test_fn, heuristic_fn):
	queue = []
	heapq.heapify(queue)
	visited = {}
	while not goal_test_fn(node):
		queue = create_children(node, actions, action_fn, cost_fn, heuristic_fn,
		                        queue)  # If not, create children of this node and add to queue.
		if len(queue) <= 0:  # If there are no prospects in the node, then no path to destination exists.
			return None
		node, queue, visited = choose_node(queue, visited)  # Get the next node to prune
	if node is not None:
		return node
	return None

'''
Wrapper function for A*.
@:param actions: The list of possible actions that can be taken.
@:param initial_node: The initial problem node from which to branch and find solutions.
@:param cost_fn: The function that is called to find out the cost of a particular action.
@:param action_fn: The function that sets the state for the child node.
@:param goal_test_fn: The goal test for each problem that tells us to stop looking for solution.
'''

def a_star(actions, initial_node, cost_fn, action_fn, goal_test_fn, heuristic_fn):
	global NODES
	NODES = 0
	return perform_a_star(actions, initial_node, cost_fn, action_fn, goal_test_fn, heuristic_fn), NODES
