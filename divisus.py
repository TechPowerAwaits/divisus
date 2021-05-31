# Copyright 2021 The divisus Authors
# SPDX-License-Identifier: EPL-2.0

import argparse
import curses.ascii
import os.path
import sys

parser = argparse.ArgumentParser(description="Converts text files to CSV.", epilog="Licensed under the EPLv2 License.")
parser.add_argument("-c", "--columns", default="3", type=int, choices=range(1,1000), metavar="[1-999]", help="how many lines to interpret as columns")
parser.add_argument("-f", "--file-type", default="text", choices=["text"], help="The format of the input file")
parser.add_argument("-v", "--version", action="version", version=os.path.basename(__file__)+" 0.1.0")
parser.add_argument("file", help="a valid input file")
args = parser.parse_args()
filepath = args.file

try:
	with open(filepath,mode="r") as stream:
		csv_out = ""
		current_col = 1
		for line in stream.read().splitlines():
			new_line = ["\""]
			nl_index = 1
			for index in range(0,len(line)):
				if curses.ascii.iscntrl(line[index]):
					new_char = ""
					# Since we are accessing a variable beyond
					# the current index, it should be checked
					# to ensure that it doesn't end up out of bounds.
					if (len(line) - 1) == index:
						pass
					elif curses.ascii.iscntrl(line[index+1]):
						pass
					elif line[index+1].isalnum():
						# Add a space to avoid having alphanumeric characters right
						# beside punctuation when control characters are removed.
						new_char = " "
					else:
						pass
				elif line[index] == "\"":
					new_char = "\'"
				else:
					new_char = line[index]
				new_line.append(new_char)
			new_line.append("\"")
			if current_col == args.columns:
				new_line.append("\n")
				current_col = 1
			else:
				new_line.append(", ")
				current_col = current_col + 1
			for element in new_line:
				csv_out = csv_out + element
		print(csv_out, end="")
except FileNotFoundError:
	print("FE: File " + os.path.abspath(filepath) + " does not exist.", file=sys.stderr)
	parser.print_usage()
except PermissionError:
	print("FE: Can't access " + os.path.abspath(filepath) + ". Please check file permissions.", file=sys.stderr)
	parser.print_usage()
except IsADirectoryError:
	print("FE: " + os.path.abspath(filepath) + " is a directory.", file=sys.stderr)
	parser.print_usage()