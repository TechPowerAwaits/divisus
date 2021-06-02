# Copyright 2021 The divisus Authors
# SPDX-License-Identifier: EPL-2.0

import argparse
import csv
import os.path
import sys

parser = argparse.ArgumentParser(description="Converts text files to CSV.", epilog="Licensed under the EPLv2 License.")
parser.add_argument("-c", "--columns", default="3", type=int, choices=range(1,1000), metavar="[1-999]", help="how many lines to interpret as columns")
parser.add_argument("-f", "--file-type", default="text", choices=["text"], help="The format of the input file")
parser.add_argument("-F" "--output-format", default="unix", choices=["excel", "unix"], help="The format of the output")
parser.add_argument("-v", "--version", action="version", version=os.path.basename(__file__)+" 0.2.0")
parser.add_argument("file", help="a valid input file")
args = parser.parse_args()
filepath = args.file
out_format = args.F__output_format

csv_dialect = ''
col_num = args.columns
if out_format == "excel":
	csv_dialect = "excel"
elif out_format == "unix":
	csv_dialect = "unix"
else:
	pass
try:
	with open(filepath,mode="r") as stream:
		csv_out = csv.writer(sys.stdout, dialect=csv_dialect)
		line_counter = 1
		csv_row = []
		for line in stream.read().splitlines():
			if line_counter == col_num:
				csv_out.writerow(csv_row)
				csv_row.clear()
				line_counter = 1
			csv_row += [line]
			line_counter += 1
except FileNotFoundError:
	print("FE: File " + os.path.abspath(filepath) + " does not exist.", file=sys.stderr)
	parser.print_usage()
except PermissionError:
	print("FE: Can't access " + os.path.abspath(filepath) + ". Please check file permissions.", file=sys.stderr)
	parser.print_usage()
except IsADirectoryError:
	print("FE: " + os.path.abspath(filepath) + " is a directory.", file=sys.stderr)
	parser.print_usage()
