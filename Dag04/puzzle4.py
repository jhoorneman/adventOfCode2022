# find overlapping cleaning schedules
# https://adventofcode.com/2022/day/4

from typing import Set, List


def pairToSets(pairString: str) -> List[Set]:
    sectionsPerElf = []
    pairString = pairString.replace('\n', '')
    for elf in pairString.split(','):
        first, second = elf.split('-')
        assignment = set(range(int(first), int(second)+1))
        assert len(assignment) > 0, 'elf must have more section assigned than 0'
        sectionsPerElf.append(assignment)
    return sectionsPerElf


def checkFullyContainedAssignments(elfSections: List[Set]) -> bool:
    assert len(elfSections) == 2, 'only comparing two elves is supported'
    overlap = elfSections[0].union(elfSections[1])
    isFullyContained = overlap == elfSections[0] or overlap == elfSections[1]
    return isFullyContained


def checkOverlap(elfSections: List[Set]) -> bool:
    assert len(elfSections) == 2, 'only comparing two elves is supported'
    overlap = elfSections[0].intersection(elfSections[1])
    return len(overlap) > 0


def main():
    with open('input.txt') as f:
        lines = f.readlines()

    numberOfContainedAssignments = 0
    numberOfOverlappingAssignments = 0
    for line in lines:
        elfSets = pairToSets(line)
        numberOfContainedAssignments += checkFullyContainedAssignments(elfSets)
        numberOfOverlappingAssignments += checkOverlap(elfSets)

    print('number of fully contained assignments')
    print(numberOfContainedAssignments)
    print('number of assignments with any overlap')
    print(numberOfOverlappingAssignments)


if __name__ == "__main__":
    main()
