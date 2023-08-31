import re
import sys
from copy import deepcopy
from numpy import fliplr, flipud
from collections import defaultdict


def day1_p1():
	depth_data = []
	with open('input_data/day1_input.txt') as infile:
		for num in infile:
			depth_data.append(int(num))
	infile.close()
	d1_p1_increasing = 0
	for x in range(1, len(depth_data), 1):
		if depth_data[x] > depth_data[x - 1]:
			d1_p1_increasing += 1
	print(f'D1P1: {d1_p1_increasing} numbers larger than the previous number')


def day1_p2():
	depth_data = []
	with open('input_data/day1_input.txt') as infile:
		for num in infile:
			depth_data.append(int(num))
	infile.close()
	d1_p2_increasing = 0
	for x in range(0, len(depth_data) - 3, 1):
		if depth_data[x] < depth_data[x + 3]:
			d1_p2_increasing += 1
	print(f'D1P2: {d1_p2_increasing} sums larger than the previous sum')


def day2_p1():
	command_data = []
	with open('input_data/day2_input.txt') as infile:
		for command in infile:
			command_data.append(command)
	infile.close()
	horizontal = 0
	depth = 0
	for x in range(len(command_data)):
		match command_data[x].split()[0]:
			case 'forward':
				horizontal += int(command_data[x].split()[1])
			case 'up':
				depth -= int(command_data[x].split()[1])
			case 'down':
				depth += int(command_data[x].split()[1])
	print(f"D2P1: {depth * horizontal} = Depth {depth} * Horizontal {horizontal}")


def day2_p2():
	command_data = []
	with open('input_data/day2_input.txt') as infile:
		for command in infile:
			command_data.append(command)
	infile.close()
	horizontal = 0
	depth = 0
	aim = 0
	for x in range(len(command_data)):
		match command_data[x].split()[0]:
			case 'forward':
				horizontal += int(command_data[x].split()[1])
				depth += aim * int(command_data[x].split()[1])
			case 'up':
				aim -= int(command_data[x].split()[1])
			case 'down':
				aim += int(command_data[x].split()[1])
	print(f"D2P2: {depth * horizontal} = Depth {depth} * Horizontal {horizontal}, with aim factored in")


def day3_p1():
	with open('input_data/day3_input.txt') as infile:
		binary_data = []
		for line in infile:
			binary_data.append(line.rstrip())
	infile.close()
	gamma_rate = []
	# find most occurring number in each position of a line of data
	for x in range(len(binary_data[0])):
		tug_of_war = 0
		for y in range(len(binary_data)):
			tug_of_war += 1 if binary_data[y][x] == '1' else -1
		gamma_rate.append('1') if tug_of_war > 0 else gamma_rate.append('0')
	epsilon_rate = []
	# use gamma to determine epsilon
	for x in range(len(gamma_rate)):
		epsilon_rate.append('1') if gamma_rate[x] == '0' else epsilon_rate.append('0')
	# convert gamma and epsilon to decimal
	dec_gamma = int(''.join([str(num) for num in gamma_rate]), 2)
	dec_epsilon = int(''.join([str(num) for num in epsilon_rate]), 2)

	print(f"D3P1: {dec_gamma * dec_epsilon} = Gamma {dec_gamma} * Epsilon {dec_epsilon}")


def reduce_array_to_one_number(binary_data, bit_criteria):
	for x in range(len(binary_data[0])):
		list_after_deletion = []
		number_to_keep = 0
		tug_of_war = 0
		for y in range(len(binary_data)):
			tug_of_war += 1 if binary_data[y][x] == '1' else -1
		if bit_criteria == 'most':
			number_to_keep = 1 if tug_of_war >= 0 else 0
		elif bit_criteria == 'least':
			number_to_keep = 0 if tug_of_war >= 0 else 1
		if len(binary_data) > 1:
			for z in range(len(binary_data)):
				if (binary_data[z])[x] == str(number_to_keep):
					list_after_deletion.append(binary_data[z])
			binary_data = list_after_deletion
	return int(''.join([str(num) for num in binary_data[0]]), 2)


def day3_p2():
	with open('input_data/day3_input.txt') as infile:
		binary_data = []
		for line in infile:
			binary_data.append(line.rstrip())
	infile.close()
	oxygen_generator_rating = reduce_array_to_one_number(binary_data, 'most')
	co2_scrubber_rating = reduce_array_to_one_number(binary_data, 'least')

	print(
		f"D3P1: {oxygen_generator_rating * co2_scrubber_rating} = Oxygen Generator Rating {oxygen_generator_rating} * CO2 Scrubber Rating {co2_scrubber_rating}")


class WinningLine:

	def __init__(self, line):
		self.line = line
		self.won = False
		self.calls_to_win = 0
		self.number_called_to_win = 0
		self.list_called_to_win = None


class BingoCard:
	def define_bingo_lines(self):
		for x in range(5):  # horizontal lines
			self.bingo_line_list.append(WinningLine(re.findall('[0-9]+', self.card[x])))
		for y in range(5):  # vertical lines
			temp_winning_line = []
			for z in range(5):
				temp_winning_line.append(re.findall('[0-9]+', self.card[z])[y])
			self.bingo_line_list.append(WinningLine(temp_winning_line))

	def set_win_info_for_card(self):
		for line in self.bingo_line_list:
			if line.won:
				if self.fastest_winning_line is None or line.calls_to_win < self.fastest_winning_line.calls_to_win:
					self.fastest_winning_line = line
					self.has_winning_line = True

	def __init__(self, card):
		self.card = card
		self.bingo_line_list = []
		self.has_winning_line = False
		self.fastest_winning_line = None

		self.define_bingo_lines()

	def process_calls(self, bingo_calls):
		for line in self.bingo_line_list:
			calls_count = 0
			match_count = 0
			call_list_to_win = []
			for call in bingo_calls:
				calls_count += 1
				call_list_to_win.append(call)
				if call in line.line:
					match_count += 1
				if match_count == len(line.line):
					line.won = True
					line.calls_to_win = calls_count
					line.number_called_to_win = call
					line.list_called_to_win = call_list_to_win
					break
		self.set_win_info_for_card()

	def print_winning_info_of_card(self):
		print(f'The fastest winning line of the card\n{self.card}\n is {self.fastest_winning_line.line} with {self.fastest_winning_line.calls_to_win} calls.')

	def compute_answer_criteria(self, day_string, criteria_string):
		sum_of_unmarked_card_numbers = 0
		for line in self.card:
			temp_line = re.findall('[0-9]+', line)
			for number in temp_line:
				if number not in self.fastest_winning_line.list_called_to_win:
					sum_of_unmarked_card_numbers += int(number)
		print(f'{day_string}: {sum_of_unmarked_card_numbers * int(self.fastest_winning_line.number_called_to_win)} = sum of unmarked numbers: {sum_of_unmarked_card_numbers} * the final number called to win: {self.fastest_winning_line.number_called_to_win} of the {criteria_string} card in the set to win')


def day4():
	# input_filename = 'input_data/day4_test_input.txt'
	input_filename = 'input_data/day4_input.txt'
	with open(input_filename) as infile:
		next(infile)
		temp_boards = infile.read().splitlines()
	with open(input_filename) as infile:
		bingo_calls = infile.readlines()[0].rstrip().split(',')
	infile.close()
	cards_list = []
	for x in range(1, len(temp_boards), 6):  # start at 1 to ignore blank line
		cards_list.append(BingoCard([temp_boards[x + y] for y in range(5)]))
	for card in cards_list:
		card.process_calls(bingo_calls)
	# Get Part 1 answer
	winning_card = None
	for card in cards_list:
		if card.has_winning_line and (winning_card is None or card.fastest_winning_line.calls_to_win < winning_card.fastest_winning_line.calls_to_win):
			winning_card = card
	winning_card.compute_answer_criteria('D4P1', 'fastest')

	# Get Part 2 answer
	winning_card = None
	for card in cards_list:
		if card.has_winning_line and (winning_card is None or card.fastest_winning_line.calls_to_win > winning_card.fastest_winning_line.calls_to_win):
			winning_card = card
	winning_card.compute_answer_criteria('D4P2', 'slowest')


class Line:
	def __init__(self, line):
		self.origin_point = line.split(' -> ')[0]
		self.terminating_point = line.split(' -> ')[1]
		self.x_origin = int(self.origin_point.split(',')[0])
		self.x_terminating = int(self.terminating_point.split(',')[0])
		self.y_origin = int(self.origin_point.split(',')[1])
		self.y_terminating = int(self.terminating_point.split(',')[1])

	def return_horizontal_and_vertical_lines(self):
		if self.x_origin == self.x_terminating or \
			self.y_origin == self.y_terminating:
			return self
		return None


class VentsMap:
	vents_map = []

	def __init__(self, length, width):
		self.vents_map = [[0 for col in range(width)] for row in range(length)]

	def add_points_to_map(self, line):
		if line.x_origin == line.x_terminating:
			if line.y_origin < line.y_terminating:
				for i in range(line.y_origin, line.y_terminating + 1):
					self.vents_map[line.x_origin][i] += 1
			else:
				for i in range(line.y_terminating, line.y_origin + 1):
					self.vents_map[line.x_origin][i] += 1
		elif line.y_origin == line.y_terminating:
			if line.x_origin < line.x_terminating:
				for j in range(line.x_origin, line.x_terminating + 1):
					self.vents_map[j][line.y_origin] += 1
			else:
				for j in range(line.x_terminating, line.x_origin+1):
					self.vents_map[j][line.y_origin] += 1
		else:
			i = line.x_origin
			j = line.y_origin
			while True:
				self.vents_map[i][j] += 1
				if i == line.x_terminating or j == line.y_terminating:
					break
				else:
					i += 1 if line.x_origin < line.x_terminating else -1
					j += 1 if line.y_origin < line.y_terminating else -1

	def compute_points_with_overlap(self):
		# for line in self.vents_map:
		# 	print(line)
		sum_of_points = 0
		for line in self.vents_map:
			for col in line:
				sum_of_points += 1 if int(col) > 1 else 0
		print(sum_of_points)


def day5():
	input_filename = 'input_data/day5_input.txt'
	# input_filename = 'input_data/day5_test_input.txt'
	with open(input_filename) as infile:
		lines = [line.rstrip() for line in infile.readlines()]
	infile.close()
	full_list_of_lines = []
	for line in lines:
		full_list_of_lines.append((Line(line)))
	# horizontal_and_vertical_lines = []
	# for line in full_list_of_lines:
	# 	if line.x_origin == line.x_terminating or line.y_origin == line.y_terminating:
	# 		horizontal_and_vertical_lines.append(line)
	# biggest_x = 0
	# biggest_y = 0
	# for line in horizontal_and_vertical_lines:
	# 	if line.x_terminating > biggest_x:
	# 		biggest_x = line.x_terminating
	# 	if line.y_terminating > biggest_y:
	# 		biggest_y = line.y_terminating
	vm = VentsMap(1000, 1000)
	# for line in horizontal_and_vertical_lines:
	for line in full_list_of_lines:
		vm.add_points_to_map(line)
	vm.compute_points_with_overlap()


class Lanternfish:
	def __init__(self, days_until_spawn):
		self.days_until_spawn = days_until_spawn


def day6():
	input_filename = 'input_data/day6_input.txt'
	# input_filename = 'input_data/day6_test_input.txt'
	with open(input_filename) as infile:
		lines = [line.rstrip() for line in infile.readlines()]
	infile.close()
	lanternfish = []
	for line in range(len(lines)):
		for num in re.findall('[0-9]+', lines[line]):
			# lanternfish.append(Lanternfish(int(num)))
			lanternfish.append(int(num))
	spawn_time_left = []
	for x in range(9):
		spawn_time_left.append(0)
	for fish in range(len(lanternfish)):
		spawn_time_left[lanternfish[fish]] += 1
	for days in range(256):
		temp_list = []
		for x in range(9):
			temp_list.append(0)
		for day in range(len(spawn_time_left)-1, -1, -1):
			if day == 0:
				temp_list[8] = temp_list[8] + spawn_time_left[0]
				temp_list[6] += spawn_time_left[0]
			else:
				temp_list[day - 1] = spawn_time_left[day]
		spawn_time_left = temp_list

	print(sum(spawn_time_left))


def move_crab_to_position_day2(initial_position, final_position):
	fuel_cost_of_move = 0
	for x in range(abs(initial_position-final_position)+1):
		fuel_cost_of_move += x
	return fuel_cost_of_move


def day7():
	input_filename = 'input_data/day7_input.txt'
	# input_filename = 'input_data/day7_test_input.txt'
	with open(input_filename) as infile:
		lines = [line.rstrip() for line in infile.readlines()]
	infile.close()
	crab_positions = []
	for line in range(len(lines)):
		for num in re.findall('[0-9]+', lines[line]):
			crab_positions.append(int(num))
	# average_position = math.ceil(sum(crab_positions) / len(crab_positions))
	range_to_vary = 10
	fuel_cost = None
	for x in range(max(crab_positions)):
		fuel_cost_of_moving_to_position = 0
		for y in range(len(crab_positions)):
			# fuel_cost_of_moving_to_position += move_crab_to_position_day1(crab_positions[y], x)
			fuel_cost_of_moving_to_position += abs(crab_positions[y], x)
		if fuel_cost is None or fuel_cost_of_moving_to_position < fuel_cost:
			fuel_cost = fuel_cost_of_moving_to_position
	print(fuel_cost)


def decode_segments(line):
	# 	0000
	#  1    2
	#  1    2
	#   3333
	#  4    5
	#  4    5
	#   6666
	number_codes = ['0' for num in range(10)]
	while '0' in number_codes:
		for input_digit in line.split(' | ')[0].split(' '):
			match len(input_digit):
				case 2:
					number_codes[1] = input_digit
				case 3:
					number_codes[7] = input_digit
				case 4:
					number_codes[4] = input_digit
				case 7:
					number_codes[8] = input_digit
		# numbers 1 4 7 8 are known
		segment_decoder = ['0' for num in range(7)]
		# able to instantly find 0 with current info
		for letter in number_codes[7]:
			if letter not in number_codes[1]:
				segment_decoder[0] = letter

		for input_digit in line.split(' | ')[0].split(' '):
			if len(input_digit) == 6:
				# could be number 0, 6, 9
				unique_segment = None
				for letter in number_codes[8]:
					if letter not in input_digit:
						# the segment not in 8
						unique_segment = letter
				if unique_segment not in number_codes[4]:
					segment_decoder[4] = unique_segment
					number_codes[9] = input_digit
				elif unique_segment not in number_codes[1]:
					segment_decoder[3] = unique_segment
					number_codes[0] = input_digit
				else:
					segment_decoder[2] = unique_segment
					number_codes[6] = input_digit

		for input_digit in line.split(' | ')[0].split(' '):
			if len(input_digit) == 2:
				segment_decoder[5] = input_digit[0] if input_digit[0] != segment_decoder[2] else input_digit[1]

		for letter in number_codes[4]:
			if letter not in segment_decoder:
				segment_decoder[1] = letter

		for letter in number_codes[8]:
			if letter not in segment_decoder:
				segment_decoder[6] = letter

		for input_digit in line.split(' | ')[0].split(' '):
			if len(input_digit) == 5:
				if segment_decoder[1] not in input_digit:
					if segment_decoder [4] not in input_digit:
						number_codes[3] = input_digit
					else:
						number_codes[2] = input_digit
				else:
					number_codes[5] = input_digit
	return number_codes


def day8():
	input_filename = 'input_data/day8_input.txt'
	# input_filename = 'input_data/day8_test_input.txt'
	# input_filename = 'input_data/day8_single_input.txt'
	with open(input_filename) as infile:
		lines = [line.rstrip() for line in infile.readlines()]
	infile.close()
	# inputs = []
	# outputs = []
	# for line in lines:
	# 	inputs.append(line.split(' | ')[0])
	# 	outputs.append(line.split(' | ')[1])

	output_sum = 0
	for line in lines:
		number_codes = decode_segments(line)
		sorted_number_codes = []
		for code in number_codes:
			sorted_number_codes.append("".join(sorted(code)))
		output_number = ''
		for output_digit in line.split(' | ')[1].split(' '):
			output_number += str(sorted_number_codes.index("".join(sorted(output_digit))))
		output_sum += int(output_number)

	print(output_sum)

	# sum_of_1_4_7_8 = 0
	# for x in range(len(outputs)):
	# 	for output in outputs[x].split(' '):
	# 		if len(output) == 2 or len(output) == 4 or len(output) == 3 or len(output) == 7:
	# 			sum_of_1_4_7_8 += 1
	# print(sum_of_1_4_7_8)


def calculate_basin_size_of_low_point(y, x, cave_map, tested_points):
	if y+x not in tested_points:
		tested_points.append(y+x)
	check_up = False
	check_down = False
	check_left = False
	check_right = False
	if int(y) > 0:
		check_up = True
	if int(y) < len(cave_map) - 1:
		check_down = True
	if int(x) > 0:
		check_left = True
	if int(x) < len(cave_map[int(y)]) - 1:
		check_right = True
	if check_up:
		if str(int(y)-1)+x not in tested_points and cave_map[int(y)-1][int(x)] < 9:
			calculate_basin_size_of_low_point(str(int(y)-1), x, cave_map, tested_points)
	if check_down:
		if str(int(y)+1)+x not in tested_points and cave_map[int(y)+1][int(x)] < 9:
			calculate_basin_size_of_low_point(str(int(y)+1), x, cave_map, tested_points)
	if check_left:
		if y+str(int(x)-1) not in tested_points and cave_map[int(y)][int(x)-1] < 9:
			calculate_basin_size_of_low_point(y, str(int(x)-1), cave_map, tested_points)
	if check_right:
		if y+str(int(x)+1) not in tested_points and cave_map[int(y)][int(x)+1] < 9:
			calculate_basin_size_of_low_point(y, str(int(x)+1), cave_map, tested_points)
	return tested_points


def day9():
	input_filename = 'input_data/day9_input.txt'
	# input_filename = 'input_data/day9_test_input.txt'
	with open(input_filename) as infile:
		lines = [line.rstrip() for line in infile.readlines()]
	infile.close()
	cave_map = []
	for line in lines:
		temp_array = []
		for num in line:
			temp_array.append(int(num))
		cave_map.append(temp_array)
	# sum = 0
	lengths = []
	for y in range(len(cave_map)):
		for x in range(len(cave_map[y])):
			low_check = 0
			proposed_low_point = cave_map[y][x]
			check_up = False
			check_down = False
			check_left = False
			check_right = False
			if y > 0:
				check_up = True
			if y < len(cave_map) - 1:
				check_down = True
			if x > 0:
				check_left = True
			if x < len(cave_map[y]) - 1:
				check_right = True
			if check_up:
				if cave_map[y-1][x] > proposed_low_point:
					low_check += 1
			else:
				low_check += 1
			if check_down:
				if cave_map[y + 1][x] > proposed_low_point:
					low_check += 1
			else:
				low_check += 1
			if check_left:
				if cave_map[y][x-1] > proposed_low_point:
					low_check += 1
			else:
				low_check += 1
			if check_right:
				if cave_map[y][x + 1] > proposed_low_point:
					low_check += 1
			else:
				low_check += 1

			tested_points = []
			if low_check == 4:
				tested_points = calculate_basin_size_of_low_point(str(y), str(x), cave_map, tested_points)
				lengths.append(len(tested_points))
	print(lengths[0])
	lengths.sort(reverse=True)
	print(lengths)
	print(lengths[0]*lengths[1]*lengths[2])


def day10_p1():
	input_filename = 'input_data/day10_input.txt'
	# input_filename = 'input_data/day10_test_input.txt'
	with open(input_filename) as infile:
		lines = [line.rstrip() for line in infile.readlines()]
	infile.close()
	incorrect_chars = []
	for line in lines:
		brack_stack = []
		for char in line:
			if char == '(' or char == '[' or char == '{' or char == '<':
				brack_stack.append(char)
			else:
				match(brack_stack.pop()):
					case '(':
						if char != ')':
							incorrect_chars.append(char)
							break
					case '[':
						if char != ']':
							incorrect_chars.append(char)
							break
					case '{':
						if char != '}':
							incorrect_chars.append(char)
							break
					case '<':
						if char != '>':
							incorrect_chars.append(char)
							break
	points = 0
	for bracket in incorrect_chars:
		match bracket:
			case ')':
				points += 3
			case ']':
				points += 57
			case '}':
				points += 1197
			case '>':
				points += 25137
	print(points)


def day10_p2():
	input_filename = 'input_data/day10_input.txt'
	# input_filename = 'input_data/day10_test_input.txt'
	with open(input_filename) as infile:
		lines = [line.rstrip() for line in infile.readlines()]
	infile.close()
	valid_lines = []
	incomplete_part_of_valid_lines = []
	for line in lines:
		valid_lines.append(line)
		brack_stack = []
		for char in line:
			if char == '(' or char == '[' or char == '{' or char == '<':
				brack_stack.append(char)
			else:
				match (brack_stack.pop()):
					case '(':
						if char != ')':
							valid_lines.pop()
							break
					case '[':
						if char != ']':
							valid_lines.pop()
							break
					case '{':
						if char != '}':
							valid_lines.pop()
							break
					case '<':
						if char != '>':
							valid_lines.pop()
							break
		if line == valid_lines[len(valid_lines)-1]:
			incomplete_part_of_valid_lines.append(brack_stack)

	scores = []
	for incomplete_line in incomplete_part_of_valid_lines:
		score = 0
		while incomplete_line:
			match incomplete_line.pop():
				case '(':
					score = (score * 5) + 1
				case '[':
					score = (score * 5) + 2
				case '{':
					score = (score * 5) + 3
				case '<':
					score = (score * 5) + 4
		scores.append(score)
	scores.sort()
	print(scores[(int(len(scores)/2))])


def flash_octopus_and_incriment_surrounding(octopi_grid, y, x):
	check_up = False
	check_down = False
	check_left = False
	check_right = False
	if y > 0:
		check_up = True
	if y < len(octopi_grid) - 1:
		check_down = True
	if x > 0:
		check_left = True
	if x < len(octopi_grid[y]) - 1:
		check_right = True
	if check_up:
		octopi_grid[y-1][x] += 1 if octopi_grid[y-1][x] != -1 else 0
		if check_left:
			octopi_grid[y-1][x-1] += 1 if octopi_grid[y-1][x-1] != -1 else 0
		if check_right:
			octopi_grid[y-1][x+1] += 1 if octopi_grid[y-1][x+1] != -1 else 0
	if check_down:
		octopi_grid[y+1][x] += 1 if octopi_grid[y+1][x] != -1 else 0
		if check_left:
			octopi_grid[y+1][x-1] += 1 if octopi_grid[y+1][x-1] != -1 else 0
		if check_right:
			octopi_grid[y+1][x+1] += 1 if octopi_grid[y+1][x+1] != -1 else 0
	if check_left:
		octopi_grid[y][x-1] += 1 if octopi_grid[y][x-1] != -1 else 0
	if check_right:
		octopi_grid[y][x+1] += 1 if octopi_grid[y][x+1] != -1 else 0


def determine_flashes(octopi_grid, flashes):
	while True:
		nine_found = False
		for y in range(len(octopi_grid)):
			for x in range(len(octopi_grid[y])):
				if octopi_grid[y][x] >= 9:
					nine_found = True
					flash_octopus_and_incriment_surrounding(octopi_grid, y, x)
					octopi_grid[y][x] = -1
		if not nine_found:
			break
	for y in range(len(octopi_grid)):
		for x in range(len(octopi_grid[y])):
			if octopi_grid[y][x] == -1:
				flashes += 1
				# octopi_grid[y][x] = 0

	return octopi_grid, flashes


def day11():
	input_filename = 'input_data/day11_input.txt'
	# input_filename = 'input_data/day11_test_input.txt'
	# input_filename = 'input_data/day11_tiny_input.txt'
	with open(input_filename) as infile:
		lines = [line.rstrip() for line in infile.readlines()]
	infile.close()
	octopi_grid = []
	simultaneous_flash_grid = []
	for line in lines:
		temp_line = []
		temp_flash_line = []
		for num in line:
			temp_line.append(int(num))
			temp_flash_line.append(0)
		octopi_grid.append(temp_line)
		simultaneous_flash_grid.append(temp_flash_line)
	flashes = 0
	step = 0
	# print(f'Before steps')
	# for y in range(len(octopi_grid)):
	# 	print(octopi_grid[y])
	# print('')
	# for step in range(10):
	while True:
		step += 1
		octopi_grid, flashes = determine_flashes(octopi_grid, flashes)
		for y in range(len(octopi_grid)):
			for x in range(len(octopi_grid[y])):
				octopi_grid[y][x]+= 1
		# print(f'Step {step + 1}')
		# for y in range(len(octopi_grid)):
		# 	print(octopi_grid[y])
		# print('')
		if octopi_grid == simultaneous_flash_grid:
			print(step)
			break
	print(flashes)


def map_paths(cave, caves_map, path_array, paths, lower_caves):
	temp_path_array = deepcopy(path_array)
	temp_path_array.append(cave)
	if temp_path_array[-1] == 'end':
		paths.append(temp_path_array)
		# print(temp_path_array)
		return
	else:
		for recurse_cave in caves_map[cave]:
			if recurse_cave != 'start':
				allow_lower_cave_to_be_checked = True
				if recurse_cave.islower():
					if recurse_cave in temp_path_array:
						for lower_cave in lower_caves:
							if temp_path_array.count(lower_cave) == 2:
								allow_lower_cave_to_be_checked = False
				if recurse_cave.isupper() or allow_lower_cave_to_be_checked:
					map_paths(recurse_cave, caves_map, temp_path_array, paths, lower_caves)
				# if recurse_cave.isupper() or recurse_cave not in temp_path_array:


def day12():
	input_filename = 'input_data/day12_input.txt'
	# input_filename = 'input_data/day12_tiny_example.txt'
	# input_filename = 'input_data/day12_middle_example.txt'
	# input_filename = 'input_data/day12_large_example.txt'
	with open(input_filename) as infile:
		lines = [line.rstrip() for line in infile.readlines()]
	infile.close()
	caves_map = {}
	lower_caves = []
	for line in lines:
		caves = line.split("-")
		if caves[0] not in caves_map:
			caves_map[caves[0]] = []
		if caves[1] not in caves_map:
			caves_map[caves[1]] = []
		caves_map[caves[0]].append(caves[1])
		caves_map[caves[1]].append(caves[0])
		if caves[0].islower() and caves[0] not in lower_caves:
			lower_caves.append(caves[0])
		if caves[1].islower() and caves[1] not in lower_caves:
			lower_caves.append(caves[1])
	paths = []
	for cave in caves_map['start']:
		path_array = []
		path_array.append('start')
		map_paths(cave, caves_map, path_array, paths, lower_caves)
	print(len(paths))


def day13():
	input_filename = 'input_data/day13_input.txt'
	# input_filename = 'input_data/day13_test_input.txt'
	with open(input_filename) as infile:
		lines = [line.rstrip() for line in infile.readlines()]
	infile.close()
	map_grid = []
	fold_instructions = []
	max_x = 0
	max_y = 0
	for line in lines:
		if line.split(' ')[0] != 'fold' and line != '':
			max_x = int(line.split(',')[0]) if int(line.split(',')[0]) > max_x else max_x
			max_y = int(line.split(',')[1]) if int(line.split(',')[1]) > max_y else max_y
		elif line.split(' ')[0] == 'fold':
			temp_fold_line = []
			temp_fold_line.append(line.split(' ')[2].split('=')[0])
			temp_fold_line.append(line.split(' ')[2].split('=')[1])
			fold_instructions.append(temp_fold_line)
	map_grid = [['.' for col in range(max_x+1)] for row in range(max_y+1)]
	for line in lines:
		if line.split(' ')[0] != 'fold' and line != '':
			map_grid[int(line.split(',')[1])][int(line.split(',')[0])] = '#'
	for instruction in fold_instructions:
		if instruction[0] == 'y':
			flipped_map_grid = flipud(map_grid)
			temp_map_grid = [['.' for col in range(len(map_grid[0]))] for row in range(int(instruction[1]))]
			for y in range(int(instruction[1])):
				for x in range(len(map_grid[y])):
					if map_grid[y][x] == '#' or flipped_map_grid[y][x] == '#':
						temp_map_grid[y][x] = '#'
			map_grid = temp_map_grid
		elif instruction[0] == 'x':
			flipped_map_grid = fliplr(map_grid)
			temp_map_grid = [['.' for col in range(int(instruction[1]))] for row in range(len(map_grid))]
			for y in range(len(map_grid)):
				for x in range(int(instruction[1])):
					if map_grid[y][x] == '#' or flipped_map_grid[y][x] == '#':
						temp_map_grid[y][x] = '#'
			map_grid = temp_map_grid

	for line in map_grid:
		temp_line = ''
		for char in line:
			temp_line += char if char == '#' else ' '
		print(temp_line)
	# count = 0
	# for line in map_grid:
	# 	count += line.count('#')
	# print(count)


def day14():
	input_filename = 'input_data/day14_input.txt'
	# input_filename = 'input_data/day14_test_input.txt'
	with open(input_filename) as infile:
		lines = [line.rstrip() for line in infile.readlines()]
	infile.close()
	template = lines[0]
	rules = {}
	for line in lines[2:]:
		rules[line.split(' -> ')[0]] = line.split(' -> ')[1]

	element_pairs_count = defaultdict(int)
	for x in range(len(template)-1):
		element_pairs_count[template[x] + template[x + 1]] += 1

	for step in range(40):
		temp_element_pairs_count = defaultdict(int)
		for key, value in element_pairs_count.items():
			temp_element_pairs_count[key[0] + rules[key]] += value
			temp_element_pairs_count[rules[key] + key[1]] += value
		element_pairs_count = temp_element_pairs_count

	single_element_count = defaultdict(int)
	for key, value in element_pairs_count.items():
		single_element_count[key[0]] += value
	single_element_count[template[-1]] += 1

	print(max(single_element_count.values())-min(single_element_count.values()))


def get_point_neighbors(node, max_graph):
	x, y = node.split(',')
	neighbors = []
	if int(y) > 0:
		neighbors.append(x + ',' + str(int(y)-1))
	if int(y) < max_graph - 1:
		neighbors.append(x + ',' + str(int(y)+1))
	if int(x) > 0:
		neighbors.append(str(int(x)-1) + ',' + y)
	if int(x) < max_graph - 1:
		neighbors.append(str(int(x)+1) + ',' + y)
	return neighbors


def dijkstra(graph, source, max_graph):
	shortest_path = defaultdict(int)
	shortest_path[source] = 0
	unvisited_nodes = []
	for entry in graph:
		if entry != source:
			shortest_path[entry] = sys.maxsize
		unvisited_nodes.append(entry)
	while unvisited_nodes:
		current_min_node = None
		for node in unvisited_nodes:
			if current_min_node is None:
				current_min_node = node
			elif shortest_path[node] < shortest_path[current_min_node]:
				current_min_node = node
		neighbors = get_point_neighbors(current_min_node, max_graph)
		for neighbor in neighbors:
			tentative_value = shortest_path[current_min_node] + graph[current_min_node]
			if tentative_value < shortest_path[neighbor]:
				shortest_path[neighbor] = tentative_value
		unvisited_nodes.remove(current_min_node)
	return shortest_path


def expand_graph(lines):
	modified_graph = [['0' for col in range(len(lines*5))] for row in range(len(lines*5))]
	for y in range(len(lines)):
		for x in range(len(modified_graph[y])):
			number_modifier = (int(x/len(lines)))
			graph_number = int(lines[y % (len(lines))][x % (len(lines))])
			for num in range(number_modifier):
				graph_number += 1
				if graph_number > 9:
					graph_number = 1
			modified_graph[y][x] = str(graph_number)
	for y in range(len(lines), len(modified_graph)):
		for x in range(len(modified_graph[y])):
			number_modifier = int(y / len(lines))
			graph_number = int(modified_graph[y % (len(lines))][x])
			for num in range(number_modifier):
				graph_number += 1
				if graph_number > 9:
					graph_number = 1
			modified_graph[y][x] = str(graph_number)

	return modified_graph


def day15():
	input_filename = 'input_data/day15_input.txt'
	# input_filename = 'input_data/day15_test_input.txt'
	with open(input_filename) as infile:
		lines = [line.rstrip() for line in infile.readlines()]
	infile.close()

	modified_graph = expand_graph(lines)
	max_graph = len(modified_graph)
	init_graph = defaultdict(int)
	for y in range(len(modified_graph)):
		for x in range(len(modified_graph[y])):
			init_graph[str(y) + "," + str(x)] = int(modified_graph[y][x])

	shortest_path = dijkstra(init_graph, '0,0', max_graph)
	print(shortest_path[str(max_graph-1) + "," + str(max_graph-1)]-int(modified_graph[0][0])+int(modified_graph[max_graph-1][max_graph-1]))


def parse_literal_value(binary_data):
	start_bit = '1'
	binary_number = ''
	while start_bit == '1':
		start_bit = binary_data[0:1]
		binary_number += binary_data[1:5]
		binary_data = binary_data[5:]
	return str(binary_data) if len(binary_data) >= 1 else '0'


def parse_packet(binary_data, version):
	if len(binary_data) > 0 and '1' in str(binary_data):
		version += int(binary_data[0:3], 2)
		print(int(binary_data[0:3], 2))
		type_id = binary_data[3:6]
		binary_data = binary_data[6:]

		decimal_id = int(type_id, 2)

		if decimal_id == 4:
			binary_data = parse_literal_value(binary_data)
		else:
			length_type_id = binary_data[0:1]
			binary_data = binary_data[1:]
			if length_type_id == '0':
				total_length = int(binary_data[0:15], 2)
				version, throwaway_binary_data = parse_packet(binary_data[15:(15+total_length)], version)
				binary_data = binary_data[15 + total_length:]
			elif length_type_id == '1':
				num_sub_packets = int(binary_data[0:11], 2)
				binary_data = binary_data[11:]
				for iteration in range(num_sub_packets):
					version, binary_data = parse_packet(binary_data, version)
		return version, binary_data if len(binary_data) >= 1 else '0'


def day16():
	# input_filename = 'input_data/day16_input.txt'
	input_filename = 'input_data/day16_test_input.txt'
	with open(input_filename) as infile:
		lines = [line.rstrip() for line in infile.readlines()]
	infile.close()

	# add 1 to beginning of hex, then strip 1 from beginning of binary to preserve leading zeroes
	hex_string = '1'
	for char in lines:
		hex_string += char
	binary_data = "{0:08b}".format(int(hex_string, 16))
	binary_data = binary_data[1:]
	# while binary_data[-1] == '0':
	# 	binary_data = binary_data.rstrip('0')

	version, binary_data = parse_packet(binary_data, 0)
	print(version)


day1_p1()
