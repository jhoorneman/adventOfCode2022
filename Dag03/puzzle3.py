# Backpack compartment control
# https://adventofcode.com/2022/day/3

from typing import List, Tuple


# To help prioritize item rearrangement, every item type can be converted to a priority:
#
# Lowercase item types a through z have priorities 1 through 26.
# Uppercase item types A through Z have priorities 27 through 52.
def itemPriority(char: str) -> int:
    assert char.isalpha(), str(char) + ' is not a letter'
    if char.islower():
        return ord(char) - 96
    else:
        return ord(char) - 38


def charsToPriority(line: str) -> List[int]:
    priority = []
    line = line.replace('\n', '')
    for char in line:
        priority.append(itemPriority(char))
    return priority


# Items of one type in 1 compartment, 2 compartments in total
def findMultipleCompartmentItems(priority: List[int]) -> int:
    assert len(priority) % 2 == 0, 'Length is not even'
    split = len(priority) // 2
    firstComp, secondComp = priority[:split], priority[split:]
    sharedItems = findSharedItems(firstComp, secondComp)
    assert len(sharedItems) == 1, 'There should be max 1 shared item we found: ' + str(sharedItems)

    return sharedItems.pop()


# badge is shared item between three lines
def findBadge(listOfItems: List[str]) -> int:
    assert len(listOfItems) == 3, 'should be presented in groups of three'
    priorityLists = []
    for items in listOfItems:
        priorityLists.append(charsToPriority(items))
    sharedItems = findSharedItems(*priorityLists)
    assert len(sharedItems) == 1, 'should be only one badge'
    return sharedItems.pop()


def findSharedItems(*priorityLists: List[int]) -> set:
    assert len(priorityLists) >= 2, 'at least two sets are needed'

    sharedItems = set(priorityLists[0])
    for priorityList in priorityLists[1:]:
        sharedItems = sharedItems.intersection(set(priorityList))

    return sharedItems


def main():
    with open('input.txt') as f:
        lines = f.readlines()

    # find incorrect items
    sumOfItems = 0
    for line in lines:
        # print(line)
        sumOfItems += findMultipleCompartmentItems(charsToPriority(line))

    # find badges
    assert len(lines) % 3 == 0, 'elves should be able to be divided in groups of three'

    badgeSum = 0
    for i in range(0, len(lines), 3):
        badgeSum += findBadge(lines[i:i+3])

    print('sum of shared items between compartments')
    print(sumOfItems)
    print('sum of badges')
    print(badgeSum)


if __name__ == "__main__":
    main()
