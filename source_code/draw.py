'''
Program to draw solution to the maze problem.
Author: Abhiram Ravi Bharadwaj
'''

import turtle as t

def _init(world_left, world_down, world_right, world_up):
	t.setworldcoordinates(world_left, world_down, world_right, world_up)
	t.tracer(0, 0)  # Set drawing mode to fast.
	t.up()
	t.backward(world_right / 2)
	t.left(90)
	t.forward(world_up / 2)
	t.right(90)

def draw_square(value, cell):
	t.down()
	if value is '1' or value is 'Q':
		t.fillcolor("black")
	elif value is 'X':
		t.fillcolor("green")
	elif value is '0' or value is '.':
		t.fillcolor("white")
	t.begin_fill()
	for i in range(4):
		t.forward(cell)
		t.left(90)
	t.end_fill()
	t.up()
	t.fillcolor("white")

def draw_maze(maze):
	cell = 20
	width = max(len(maze), len(maze[0])) * 1.5 * cell
	_init(-width, -width, width, width)
	for row in maze:
		for value in row:
			draw_square(value, cell)
			t.forward(cell)
		t.backward(cell * len(maze[0]))
		t.right(90)
		t.forward(cell)
		t.left(90)
	t.update()
	t.mainloop()
