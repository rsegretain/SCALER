import argparse
import csv
import math
import time
import numpy as np
from numpy import random

def noise_f(value, scale, ceil, floor):
	new_value = value + random.normal(0, scale, 1)

	if new_value > ceil:
		new_value = ceil
	
	if new_value < floor:
		new_value = floor

	return new_value 


def sin_f(x, ceil=100, floor=0, peak_nb=4, d=1800, h_offset=0, noise=False):
	f = peak_nb / d
	fun_freq = 2 * math.pi * f
	amp = (ceil - floor) / 2
	v_offset = amp + floor

	v = amp * math.sin(fun_freq * x + h_offset) + v_offset

	if noise:
		v = noise_f(v, 0.1 * amp, ceil, floor)

	return v


def abs_sin_f(x, ceil=100, floor=0, peak_nb=4, d=1800, h_offset=0, noise=False):
	f = (peak_nb/2) / d
	fun_freq = 2 * math.pi * f
	amp = ceil - floor
	v_offset = floor

	v = abs( amp * math.sin(fun_freq * x + h_offset)) + v_offset

	if noise:
		v = noise_f(v, 0.1 * amp, ceil, floor)

	return v


def cos_f(x, ceil=100, floor=0, peak_nb=4, d=1800, h_offset=0, noise=False):
	f = (peak_nb-1) / d
	fun_freq = 2 * math.pi * f
	amp = (ceil - floor) / 2
	v_offset = amp + floor

	v = amp * math.cos(fun_freq * x + h_offset) + v_offset

	if noise:
		v = noise_f(v, 0.1 * amp, ceil, floor)

	return v


def abs_cos_f(x, ceil=100, floor=0, peak_nb=4, d=1800, h_offset=0, noise=False):
	f = (peak_nb-1)/2 / d
	fun_freq = 2 * math.pi * f
	amp = ceil - floor
	v_offset = floor

	v = abs( amp * math.cos(fun_freq * x + h_offset)) + v_offset

	if noise:
		v = noise_f(v, 0.1 * amp, ceil, floor)

	return v


def linear_f(x, a=0.1, ceil=250, floor=5, noise=False):
	v =  a * x + floor

	if (noise and a > 0):
		v = noise_f(v, 10*a, ceil, floor)
	elif (noise and a < 0):
		v = noise_f(v, -10*a, floor, ceil)

	if (v > ceil and a > 0) or (v < ceil and a < 0):
		v = ceil

	return v

def linear_floor_to_ceil(x, duration, floor=5, ceil=250, noise=False):
	a = (ceil - floor) / duration
	v =  a * x + floor

	if (noise and a > 0):
		v = noise_f(v, 10*a, ceil, floor)
	elif (noise and a < 0):
		v = noise_f(v, -10*a, floor, ceil)

	if (v > ceil and a > 0) or (v < ceil and a < 0):
		v = ceil

	return v


def log_f(x, a=1, ceil=100, floor=5, noise=False):
	if (x <= 0):
		v = floor
	else:
		v = a * math.log(x) + floor

	if (noise and a > 0):
		v = noise_f(v, 2, ceil, floor)
	elif (noise and a < 0):
		v = noise_f(v, 2, floor, ceil)

	if (v > ceil and a > 0) or (v < ceil and a < 0):
		v = ceil

	return v


def bell_f(x, ceil=100, floor=5):
	mean = (ceil - floor) / 2 + floor
	std_dev = (ceil - floor) / 6

	v = random.normal(loc=mean, scale=std_dev, size=1)

	return v


def rd_jump(x, ceil=100, floor=5, duration=1800):
	np.random.seed(int(time.time()))

	jump_start = np.random.uniform(0, duration//2)
	jump_end = jump_start + duration // 3

	ret = floor
	if x >= jump_start and x <= jump_end:
		ret = ceil

	return ret


def rd_stairs(x, ceil=100, floor=5, duration=1800, nb_steps=5):
	np.random.seed(1)

	step_size = duration // nb_steps

	random_stairs = np.random.uniform(low=floor, high=ceil, size=nb_steps)

	stair_idx = int(x // step_size)

	return random_stairs[stair_idx]


def mystery_box_f(x, window=10, ceil= 100, floor=0, d=1800, noise=False):
	'''
	Don't try to understand the mystery box.
	'''
	box = [sin_f, linear_f, bell_f, cos_f, log_f]

	i = math.floor(x / window) % len(box)

	return box[i](x)


def const_f(x, ceil=100):
	return ceil


def stairs_up(x, ceil=100, floor=5, d=1800, nb_steps=5):
	step = math.floor((ceil-floor) / (nb_steps-1))
	mult = math.floor(nb_steps * x / d)

	return  floor + step * mult


def stairs_down(x, ceil=100, floor=5, d=1800, nb_steps=5):
	step = math.floor((ceil-floor) / (nb_steps-1))
	mult =  math.floor(nb_steps * x / d)

	return  ceil - step * mult


def generate_csv_file(filename, duration, load_intensity_function, step=1):
	with open(filename, mode='w', newline='') as file:
		writer = csv.writer(file)
		for i in range(0, duration, step):
			timestamp = 0.5 + i
			load_intensity = load_intensity_function(i)  # Call user-specified function
			writer.writerow([timestamp, int(load_intensity)])

def main():
	parser = argparse.ArgumentParser(description='Generate a CSV file with load intensity data.')
	parser.add_argument('-f', '--filename', type=str, default='intensity.csv', help='Name of the csv file to be generated.')
	parser.add_argument('-g', '--function', type=str, choices=['sin', 'cos', 'abscos', 'abssin', 'linear', 'linear_perso', 'log', 'bell', 'rdjump', 'rdstairs', 'mysterybox', 'const', 'stairsu', 'stairsd'], default='sin', help='Name of the function to generate load intensity data.')
	parser.add_argument('-t', '--duration', type=int, default=1800, help='Duration of intervals to generate in seconds.')
	parser.add_argument('--ceil', type=int, default=100, help='Upper limit.')
	parser.add_argument('--floor', type=int, default=0, help='Lower limit.')
	parser.add_argument('-p', '--peaks', type=int, default=4, help='Number of peaks for sin/cos functions.')
	parser.add_argument('-a', '--inclination', type=float, default=0.1, help='Inclination for linear functions.')
	parser.add_argument('-n', '--noise', action='store_true', default=False, help='Flag to add noise to the generated intensity data.')
	parser.add_argument('-s', '--step', type=int, default=1, help='step between load generations')
	parser.add_argument('-S', '--stairsstep', type=int, default=5, help='Number of step for stairs functions')
	args = parser.parse_args()

	# Duration time argument
	duration = args.duration
	limit_max = args.ceil
	limit_min = args.floor
	peak_number = args.peaks
	inclination = args.inclination
	noise = args.noise
	step = args.step
	stairsstep = args.stairsstep

	# Get the user-specified load intensity function
	if args.function == 'sin':
		load_intensity_function = lambda x: sin_f(x, ceil=limit_max, floor=limit_min, peak_nb=peak_number, d=duration, noise=noise)
	elif args.function == 'abssin':
		load_intensity_function = lambda x: abs_sin_f(x, ceil=limit_max, floor=limit_min, peak_nb=peak_number, d=duration, noise=noise)
	elif args.function == 'cos':
		load_intensity_function = lambda x: cos_f(x, ceil=limit_max, floor=limit_min, peak_nb=peak_number, d=duration, noise=noise)
	elif args.function == 'abscos':
		load_intensity_function = lambda x: abs_cos_f(x, ceil=limit_max, floor=limit_min, peak_nb=peak_number, d=duration, noise=noise)
	elif args.function == 'linear':
		load_intensity_function = lambda x: linear_f(x, a=inclination, ceil=limit_max ,floor=limit_min, noise=noise)
	elif args.function == 'linear_perso':
		load_intensity_function = lambda x: linear_floor_to_ceil(x, duration=duration, ceil=limit_max+1 ,floor=limit_min, noise=noise)
	elif args.function == 'log':
		load_intensity_function = lambda x: log_f(x, a=inclination, ceil=limit_max, floor=limit_min, noise=noise)
	elif args.function == 'bell':
		load_intensity_function = lambda x: bell_f(x, ceil=limit_max, floor=limit_min)
	elif args.function == 'mysterybox':
		load_intensity_function = lambda x: mystery_box_f(x)
	elif args.function == 'const':
		load_intensity_function = lambda x: const_f(x, ceil=limit_max)
	elif args.function == "stairsu":
		load_intensity_function = lambda x: stairs_up(x, ceil=limit_max, floor=limit_min, d=duration, nb_steps=stairsstep)
	elif args.function == "stairsd":
		load_intensity_function = lambda x: stairs_down(x, ceil=limit_max, floor=limit_min, d=duration, nb_steps=stairsstep)
	elif args.function == "rdstairs":
		load_intensity_function = lambda x: rd_stairs(x, ceil=limit_max, floor=limit_min, duration=duration, nb_steps=stairsstep)
	elif args.function == "rdjump":
		load_intensity_function = lambda x: rd_jump(x, ceil=limit_max, floor=limit_min, duration=duration)
	else:
		print('Invalid function name. Use one of the following ["sin", "cos", "abscos", "abssin", "linear", "log", "bell", "mysterybox"]')
		return

	# Generate the CSV file
	generate_csv_file(args.filename, duration, load_intensity_function, step)

if __name__ == '__main__':
	main()
