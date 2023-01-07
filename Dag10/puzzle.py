# parsing instructions
# https://adventofcode.com/2022/day/10

from typing import List


def parseInstructions(lines: List[str]) -> List[int]:
    instructions = [0]
    for i, line in enumerate(lines):
        if "noop" in line:
            instructions.append(0)
        elif "addx" in line:
            splitLine = line.split()
            instructions.append(0)
            instructions.append(int(splitLine[1]))
    return instructions


def processInstructions(instructions: List[int]) -> List[int]:
    # add two "standard entries" so that the indexes for determining the pointsOfInterest work out
    registerX = [1, 1]
    for i, instruction in enumerate(instructions):
        if i != 0:
            registerX.append(registerX[-1] + instruction)
        else:
            assert instruction == 0, "first instruction should always be do nothing which is represented as 0"
    return registerX


def main():
    with open('input.txt') as f:
        lines = f.readlines()
    instructions = parseInstructions(lines)
    registerX = processInstructions(instructions)
    pointsOfInterest = [20, 60, 100, 140, 180, 220]
    for i in pointsOfInterest:
        print(registerX[i])
    signalStrength = sum([POI * registerX[POI] for POI in pointsOfInterest])
    print("Signal strenght is", signalStrength)


if __name__ == "__main__":
    main()
