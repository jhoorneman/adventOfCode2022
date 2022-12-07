# manipulate stacking crates in order
# https://adventofcode.com/2022/day/5
from copy import deepcopy
from typing import List


def parseInitialCrates(lines: List[str]) -> List[str]:
    maxStacks = 10
    stacks = [''] * maxStacks
    for line in lines:
        # check for crates
        if '[' in line:
            for i in range(0, len(line), 4):
                # get crate part for example '[C]'
                crate = line[i:i+3].replace('[', '').replace(']', '').replace(' ', '')
                stacks[i//4] += crate
    # stacks are listed from top to bottom. So at index 0 is the topmost crate
    return stacks


def parseMoveRules(lines: List[str]) -> List[dict]:
    moveRules = []
    for line in lines:
        # check if it is a move rule
        if 'move' in line:
            # move rule split for example from 'move 1 from 1 to 2' to ['move', '1', 'from', '1', 'to', '2']
            split = line.split()
            moveRules.append({'num': int(split[1]), 'from': int(split[3]) - 1, 'to': int(split[5]) - 1})
    return moveRules


def giveTopCrates(stacks: List[str]) -> str:
    topCrates = ''
    for stack in stacks:
        if len(stack) > 0:
            topCrates += stack[0]

    return topCrates


def applyMoveRule(stacks: List[str], moveRule: dict, invertStacks: bool):
    # move a number of crates from one stack to other
    crates = stacks[moveRule['from']][:moveRule['num']]
    # remove crates
    stacks[moveRule['from']] = stacks[moveRule['from']][moveRule['num']:]
    # place on new stack other way around
    if invertStacks:
        stacks[moveRule['to']] = crates[::-1] + stacks[moveRule['to']]
    else:
        stacks[moveRule['to']] = crates + stacks[moveRule['to']]


def applyMoveRules(stacks: List[str], moveRules: List[dict], invertStacks: bool):
    for moveRule in moveRules:
        applyMoveRule(stacks, moveRule, invertStacks)


def main():
    with open('input.txt') as f:
        lines = f.readlines()

    stacks = parseInitialCrates(lines)
    moveRules = parseMoveRules(lines)
    mover9000 = deepcopy(stacks)
    applyMoveRules(mover9000, moveRules, True)
    mover9001 = deepcopy(stacks)
    applyMoveRules(mover9001, moveRules, False)

    print('start situation')
    print(stacks)
    print('final situation CrateMover 9000')
    print(mover9000)
    print('top crates CrateMover 9000')
    print(giveTopCrates(mover9000))
    print('final situation CrateMover 9001')
    print(mover9001)
    print('top crates CrateMover 9001')
    print(giveTopCrates(mover9001))


if __name__ == "__main__":
    main()
