#
# https://adventofcode.com/2022/day/8
from copy import copy
from typing import List, Tuple, Dict


TreeLine = List[int]
TreeGrid = List[TreeLine]
VisibilityLine = List[bool]
VisibilityMask = List[VisibilityLine]
ViewLine = List[int]
ViewMask = List[ViewLine]


def parseTrees(lines: List[str]) -> TreeGrid:
    treeGrid = []
    for line in lines:
        treeLine = list(line.strip())
        treeLine = [int(x) for x in treeLine]
        treeGrid.append(treeLine)
    return treeGrid


def createMask(treeGrid: TreeGrid, fillWith) -> List[list]:
    width = len(treeGrid[0])
    height = len(treeGrid)
    maks = []
    row = [fillWith]*width
    [maks.append(copy(row)) for i in range(height)]
    return maks


def createVisibilityMask(treeGrid: TreeGrid) -> VisibilityMask:
    return createMask(treeGrid, False)


def createViewMask(treeGrid: TreeGrid) -> ViewMask:
    return createMask(treeGrid, 1)


def checkVisibilityOneDirection(treeLine: TreeLine, visibilityLine: VisibilityLine, reverse: bool = False) -> VisibilityLine:
    assert len(treeLine) == len(visibilityLine), 'treeGrid and visiblityMask should be same size'
    if not reverse:
        iterateOver = range(len(treeLine))
    else:
        iterateOver = range(len(treeLine))[::-1]

    highestTree = -1
    for i in iterateOver:
        if treeLine[i] > highestTree:
            highestTree = treeLine[i]
            visibilityLine[i] = True
    return visibilityLine


def checkViewOneDirection(fromTree: int, treeLine: TreeLine, viewLine: ViewLine, reverse: bool = False) -> int:
    assert len(treeLine) == len(viewLine), 'treeGrid and viewMask should be same size'
    if not reverse:
        iterateOver = range(fromTree, len(treeLine))[1:]
    else:
        # from the tree to -1 with steps of -1. To -1 so that index of 0 will be included
        iterateOver = range(fromTree, -1, -1)[1:]
    
    if viewLine[fromTree] == 0:
        # it will always stay 0 no need to calculate
        return 0
    else:
        view = 0
        treeHeight = treeLine[fromTree]
        for i in iterateOver:
            if treeLine[i] < treeHeight:
                view += 1
            else:
                view += 1
                break
    return view


def checkVisibility(treeGrid: TreeGrid) -> VisibilityMask:
    visibilityMask = createVisibilityMask(treeGrid)
    for i in range(len(treeGrid)):
        checkVisibilityOneDirection(treeGrid[i], visibilityMask[i])
        checkVisibilityOneDirection(treeGrid[i], visibilityMask[i], True)
    for j in range(len(treeGrid[0])):
        treeLine = [row[j] for row in treeGrid]
        visibilityLine = [row[j] for row in visibilityMask]
        visibilityLine = checkVisibilityOneDirection(treeLine, visibilityLine)
        insertVerticalVisibilityInformation(j, visibilityLine, visibilityMask)
        visibilityLine = checkVisibilityOneDirection(treeLine, visibilityLine, True)
        insertVerticalVisibilityInformation(j, visibilityLine, visibilityMask)

    return visibilityMask


def checkView(treeGrid: TreeGrid) -> ViewMask:
    def insertViewInformation(row: int, column: int, view: int):
        viewMask[row][column] *= view

    viewMask = createViewMask(treeGrid)
    width = len(treeGrid[0])
    height = len(treeGrid)
    for i in range(height):
        for j in range(width):
            view = checkViewOneDirection(j, treeGrid[i], viewMask[i])
            insertViewInformation(i, j, view)
            view = checkViewOneDirection(j, treeGrid[i], viewMask[i], True)
            insertViewInformation(i, j, view)

    for j in range(width):
        treeLine = [row[j] for row in treeGrid]
        viewLine = [row[j] for row in viewMask]
        for i in range(height):
            view = checkViewOneDirection(i, treeLine, viewLine)
            insertViewInformation(i, j, view)
            view = checkViewOneDirection(i, treeLine, viewLine, True)
            insertViewInformation(i, j, view)

    return viewMask


def insertVerticalVisibilityInformation(column: int, visibilityLine: VisibilityLine, visibilityMask: VisibilityMask) -> VisibilityMask:
    for i in range(len(visibilityLine)):
        visibilityMask[i][column] = visibilityMask[i][column] or visibilityLine[i]

    return visibilityMask


def printMatrix(matrix: List[list]) -> None:
    for row in matrix:
        print(row)


def main():
    with open('input.txt') as f:
        lines = f.readlines()
    treeGrid = parseTrees(lines)
    visibilityMask = checkVisibility(treeGrid)
    print('visibility after check')
    printMatrix(visibilityMask)
    print('count visible trees')
    print(sum(sum(row) for row in visibilityMask))

    viewMask = checkView(treeGrid)
    print('Trees')
    printMatrix(treeGrid)
    print('View')
    printMatrix(viewMask)
    print('Highest possible score')
    print(max(max(row) for row in viewMask))


if __name__ == "__main__":
    main()
