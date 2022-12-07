# start op packet marker in communication
# https://adventofcode.com/2022/day/6


def isEachCharUnique(chars: str) -> bool:
    return len(set(chars)) == len(chars)


# returns index of first character after the unique four characters
def findFirstXUnique(chars: str, x: int) -> int:
    for i in range(len(chars)):
        if isEachCharUnique(chars[i:i+x]):
            return i+x


def main():
    with open('input.txt') as f:
        lines = f.readlines()

    for line in lines:
        print('first 04 unique: ' + str(findFirstXUnique(line, 4)))
        print('first 14 unique: ' + str(findFirstXUnique(line, 14)))


if __name__ == "__main__":
    main()
