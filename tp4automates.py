#!/usr/bin/env python3
import sys
import reg_exp

usage_str = f'Usage: {sys.argv[0]} <regular_expression> <word_to_recognize>'

if len(sys.argv) != 3:
    print('Error: Invalid number of arguments.', file = sys.stderr)
    print(usage_str)
    sys.exit()
_, regular_expression, word = sys.argv
print('YES' if reg_exp.is_recognized(regular_expression, word) else 'NO')