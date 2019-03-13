'''
Base node class for AI problems
'''

class Node:
	__slots__ = 'state_config', 'parent', 'action', 'children'

	def __init__(self, state_config, parent=None, action=None):
		self.state_config = state_config
		self.parent = parent
		self.action = action
		self.children = []

	def __eq__(self, other):
		retval = self.state_config['current_pos'] == other.state_config['current_pos']
		if self.state_config['problem'] == 'n-queen':
			retval &= self.state_config['blocked'] == other.state_config['blocked']
		return retval

	def __lt__(self, other):
		if 'cost' in self.state_config:
			return self.state_config['cost'] - other.state_config['cost']
		return -1

	def __str__(self):
		result = ''
		for line in self.state_config:
			result = result + str(line) + '\n'
		return result
