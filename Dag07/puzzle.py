# parse file system output
# https://adventofcode.com/2022/day/7

from typing import List, Dict, Tuple, Any, Union

Cmd = Dict[str, Union[str, List[str]]]
CmdList = List[Cmd]


def isCommand(line: str) -> bool:
    return line[0] == '$'


def isDir(line: str) -> bool:
    return line[:3] == 'dir'


def parseCmdInput(lines: List[str]) -> CmdList:
    cmdList = []
    tmpCommand = {}
    for line in lines:
        if isCommand(line):
            # write previous command to cmdList
            if len(tmpCommand) > 0:
                cmdList.append(tmpCommand)
            tmpCommand = {'cmd': line.replace('$', '').strip(), 'out': []}
        else:
            tmpCommand['out'].append(line)
    # append last command
    if len(tmpCommand) > 0:
        cmdList.append(tmpCommand)
    return cmdList


def cmdCd(cmd: Cmd, currentPath: str) -> str:
    arg = cmd['cmd'].split()[1]
    if arg == '/':
        currentPath = 'home'
    elif arg == '..':
        currentPath = '/'.join(currentPath.split('/')[:-1])
    else:
        currentPath = currentPath + '/' + arg
    return currentPath


def cmdLs(cmd: Cmd) -> dict:
    content = cmd['out']
    subFilesystem = {}
    for item in content:
        if 'dir' in item:
            subFilesystem['/' + item.split()[1]] = {}
        else:
            # item is a file for example '8033020 d.log'
            file = item.split()
            subFilesystem[file[1]] = int(file[0])
    return subFilesystem

# def dictItemFromPath(path: str, filesystem: dict) -> Any[dict, list]:
#     pathList = path.split('/')
#     raise NotImplementedError


def currentDir(path: str) -> str:
    return '/' + path.split('/')[-1]


def updateFilesystem(path: str, filesystem: dict, content: dict = None) -> dict:
    if content is None:
        content = {}
    subFs = filesystem
    dirs = path.split('/')
    for i, _dir in enumerate(dirs):
        # add / back so it is recognisable as directory
        _dir = '/' + _dir
        if _dir not in subFs:
            subFs[_dir] = {}
        if i == len(dirs) -1:
            # merge new content with old information, prioritize old information
            subFs[_dir] = content | subFs[_dir]
        else:
            subFs = subFs[_dir]

    return filesystem


def cmdListToFilesystem(cmdList: CmdList) -> dict:
    currentPath = ''
    filesystem = {}
    # pathsAdded = []
    for cmd in cmdList:
        if 'cd' in cmd['cmd']:
            currentPath = cmdCd(cmd, currentPath)
            updateFilesystem(currentPath, filesystem)
            # pathsAdded.append(currentPath)
        elif 'ls' in cmd['cmd']:
            content = cmdLs(cmd)
            updateFilesystem(currentPath, filesystem, content)

    # for path in pathsAdded:
    #     assert doesPathExist(path, filesystem), 'path ' + path + ' was added before but isn\'t here anymore'
    return filesystem


def findDirSizes(filesystem: dict, dirSizes: Dict[str, int] = None, currentPath: str = '') -> Dict[str, int]:
    if dirSizes is None:
        dirSizes = {}
    if currentPath not in dirSizes:
        dirSizes[currentPath] = 0
    for item in filesystem:
        if '/' in item:
            # this is a directory
            findDirSizes(filesystem[item], dirSizes, currentPath + item)
            dirSizes[currentPath] += dirSizes[currentPath + item]
        else:
            dirSizes[currentPath] += filesystem[item]
    if currentPath == '':
        del dirSizes['']
    return dirSizes


def findDirsSmallerThan(maxSize: int, filesystem: dict) -> Dict[str, int]:
    dirSizes = findDirSizes(filesystem)
    for _dir in list(dirSizes.keys()):
        if dirSizes[_dir] > maxSize:
            del dirSizes[_dir]
    return dirSizes


def findDirsBiggerThan(minSize: int, filesystem: dict) -> Dict[str, int]:
    dirSizes = findDirSizes(filesystem)
    for _dir in list(dirSizes.keys()):
        if dirSizes[_dir] < minSize:
            del dirSizes[_dir]
    return dirSizes


def doesPathExist(path: str, filesystem: dict) -> bool:
    dirs = path.split('/')
    assert dirs[0] == 'home'
    subFs = filesystem
    for _dir in dirs:
        _dir = '/' + _dir
        if _dir not in subFs:
            return False
        else:
            subFs = subFs[_dir]
    return True


def main():
    with open('input.txt') as f:
        lines = f.readlines()

    cmdList = parseCmdInput(lines)
    filesystem = cmdListToFilesystem(cmdList)
    fileSizes = findDirSizes(filesystem)
    properDirs = findDirsSmallerThan(100000, filesystem)
    print('Directories smaller than 100000 found: ')
    for item in properDirs:
        print(item + ": " + str(properDirs[item]))
    print('Total size')
    print(sum(properDirs.values()))
    print('Size of home is:', fileSizes['/home'])
    sizeToFreeUp = fileSizes['/home'] - int(40e6)
    print('Max size before update is 40000000, so we are', sizeToFreeUp, 'over')
    deletableDirs = findDirsBiggerThan(sizeToFreeUp, filesystem)
    print('Directories bigger than', sizeToFreeUp, 'found: ')
    for item in deletableDirs:
        print(item + ": " + str(deletableDirs[item]))
    print('Smallest of those is')
    print(min(deletableDirs.values()))


if __name__ == "__main__":
    main()
