# Count calories
# https://adventofcode.com/2022/day/1

import ast
import numpy as np
with open('input.txt') as f:
    text = f.read()

# parse input to list
listtext = '[['+text.replace('\n\n', '], [').replace('\n', ', ')+']]'
elves = ast.literal_eval(listtext)
calorieTotals = np.zeros(len(elves), dtype='int')
for i, elf in enumerate(elves):
    calorieTotals[i] = sum(elf)

calorieTotals.sort()

# calories top elf
print(calorieTotals[-1])

# calories top three elves
print(sum(calorieTotals[-3:]))