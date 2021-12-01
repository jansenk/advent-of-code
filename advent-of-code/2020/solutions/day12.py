from ..util import Point, moven, move, Direction, manhattan_distance

def travel(filename):
	# import pdb; pdb.set_trace()
	start_point = Point(0,0)
	current_point = start_point
	current_heading = Direction.RIGHT
	for line in open('advent/input_files/' + filename):
		command = line[0]
		value = int(line[1:])
		prev_point, prev_heading = current_point, current_heading
		assert command in 'NSEWLRF'
		if command == 'N':
			current_point = moven(current_point, Direction.UP, value)
		elif command == 'S':
			current_point = moven(current_point, Direction.DOWN, value)
		elif command == 'E':
			current_point = moven(current_point, Direction.RIGHT, value)
		elif command == 'W':
			current_point = moven(current_point, Direction.LEFT, value)
		elif command == 'L':
			assert value % 90 == 0
			current_heading = Direction.rotate_cardinal(current_heading, -int(value / 90))
		elif command == 'R':
			assert value % 90 == 0
			current_heading = Direction.rotate_cardinal(current_heading, int(value / 90))
		elif command == 'F':
			current_point = moven(current_point, current_heading, value)
		print(f'{command}{value}: {prev_point} @ {Direction.name(prev_heading)} -> {current_point} @ {Direction.name(current_heading)}')
	print(manhattan_distance(current_point, start_point))

# travel('12.txt')

def travel2(filename):
	# import pdb; pdb.set_trace()
	start_point = Point(0,0)
	waypoint = Point(10, 1)
	current_point = start_point
	current_heading = Direction.RIGHT
	for line in open('advent/input_files/' + filename):
		command = line[0]
		value = int(line[1:])
		prev_point, prev_heading, prev_waypoint = current_point, current_heading, waypoint
		assert command in 'NSEWLRF'
		if command == 'N':
			waypoint = moven(waypoint, Direction.UP, value)
		elif command == 'S':
			waypoint = moven(waypoint, Direction.DOWN, value)
		elif command == 'E':
			waypoint = moven(waypoint, Direction.RIGHT, value)
		elif command == 'W':
			waypoint = moven(waypoint, Direction.LEFT, value)
		elif command == 'L':
			assert value % 90 == 0
			steps_left = int(value / 90) % 4
			# up : 1, 100
			# left : -100, 1
			# down: -1, -100
			# right: 100, -1
			for _ in range(steps_left):
				waypoint = Point(-waypoint.y, waypoint.x)
		elif command == 'R':
			assert value % 90 == 0
			steps_right = int(value / 90) % 4
			# up : 1, 100
			# left : -100, 1
			# down: -1, -100
			# right: 100, -1
			for _ in range(steps_right):
				waypoint = Point(waypoint.y, -waypoint.x)
		elif command == 'F':
			current_point = moven(current_point, waypoint, value)
		print(f'{command}{value}: {prev_point} @ {Direction.name(prev_heading)} [{prev_waypoint}]-> {current_point} @ {Direction.name(current_heading)} [{waypoint}]')
	print(manhattan_distance(current_point, start_point))

travel2('12.txt')