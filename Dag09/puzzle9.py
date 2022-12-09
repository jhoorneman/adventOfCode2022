# tail following head of rope
# https://adventofcode.com/2022/day/9
import math
from typing import Dict, Union, List, Set, Tuple

Rule = Dict[str, Union[str, int]]
Rules = List[Rule]
Position = Dict[str, int]
Rope = List[Position]


def parseRule(line: str) -> Rule:
    line = line.strip()
    ruleParts = line.split()
    return {'cmd': ruleParts[0], 'repeat': int(ruleParts[1])}


def parseRules(lines: List[str]) -> Rules:
    rules = []
    for line in lines:
        rules.append(parseRule(line))
    return rules


def knotDistance(rope: Rope) -> float:
    assert len(rope) == 2, 'rope has to be length 2'
    return (absPosDiff(rope, 'x') ** 2 + absPosDiff(rope, 'y') ** 2) ** .5


def absPosDiff(rope: Rope, direction: str) -> int:
    assert len(rope) == 2, 'rope has to be length 2'
    assert direction == 'x' or direction == 'y', 'only x or y allowed as direction'
    return abs(rope[0][direction] - rope[1][direction])


def moveFollowingKnot(rope: Rope, direction: str) -> None:
    assert direction == 'x' or direction == 'y', 'only x or y allowed as direction'
    assert len(rope) == 2, 'rope has to be length 2'
    diff = absPosDiff(rope, direction)
    if diff == 2:
        rope[1][direction] = (rope[0][direction] - rope[1][direction])//2 + rope[1][direction]
    elif diff == 1:
        rope[1][direction] = rope[0][direction]
    elif diff == 0:
        pass
    else:
        raise AssertionError('difference between knots should not be more than 2 in one direction')


def updateFollowingKnotPosition(rope: Rope) -> None:
    assert len(rope) == 2, 'rope has to be length 2'
    dist = knotDistance(rope)
    if dist < 2:
        pass
    elif math.isclose(dist, 2):
        if absPosDiff(rope, 'x') == 2:
            moveFollowingKnot(rope, 'x')
        else:
            moveFollowingKnot(rope, 'y')
    elif dist > 2:
        moveFollowingKnot(rope, 'x')
        moveFollowingKnot(rope, 'y')


def moveLeadingKnot(leadingKnot: Position, command: str) -> Position:
    if command == 'R':
        leadingKnot['x'] += 1
    elif command == 'L':
        leadingKnot['x'] -= 1
    elif command == 'U':
        leadingKnot['y'] += 1
    elif command == 'D':
        leadingKnot['y'] -= 1
    else:
        raise AssertionError("command should be R, L, U or D")
    return leadingKnot


def simulateRule(rule: Rule, rope: Rope) -> Set[str]:
    tailPositions = {str(rope[-1])}
    for i in range(rule['repeat']):
        leadingKnot = rope[0]
        moveLeadingKnot(leadingKnot, rule['cmd'])
        for knot in rope[1:]:
            updateFollowingKnotPosition([leadingKnot, knot])
            leadingKnot = knot
        tailPositions.add(str(rope[-1]))
    return tailPositions


def simulateRules(rules: Rules, ropeLength: int) -> Set[str]:
    rope = [{'x': 0, 'y': 0} for _ in range(ropeLength)]
    tailPositions = {str(rope[-1])}
    for rule in rules:
        newTailPositions = simulateRule(rule, rope)
        tailPositions = tailPositions.union(newTailPositions)
    return tailPositions


def main():
    with open('input.txt') as f:
        lines = f.readlines()
    rules = parseRules(lines)
    shortTailPositions = simulateRules(rules, 2)
    longTailPositions = simulateRules(rules, 10)
    # for rule in rules:
    #     print(rule)
    # for tailPos in tailPositions:
    #     print(tailPos)
    print('number of places visited by tail of short rope')
    print(len(shortTailPositions))
    print('number of places visited by tail of long rope')
    print(len(longTailPositions))


if __name__ == "__main__":
    main()
