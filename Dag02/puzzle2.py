# Rock paper scissor matchStrategyWrong guide
# https://adventofcode.com/2022/day/2

# set rules of rock, paper, scissors (you are the second letter): R, P, S
wins = ['R P', 'P S', 'S R']
ties = ['R R', 'P P', 'S S']
# losses is wins but the other way around
losses = [w[::-1] for w in wins]

# dictionaries
winDict = {item[0]: item[1] for item in [win.split() for win in wins]}
loseDict = {item[0]: item[1] for item in [lose.split() for lose in losses]}
tieDict = {item[0]: item[1] for item in [tie.split() for tie in ties]}
shapePoints = {'R': 1, 'P': 2, 'S': 3}


# count score
# For shape you selected (1 for Rock, 2 for Paper, and 3 for Scissors)
# plus the score for the outcome of the round (0 if you lost, 3 if the round was a draw, and 6 if you won)
def countScore(_match):
    score = 0
    if _match in wins:
        score += 6
    elif _match in ties:
        score += 3
    elif _match in losses:
        score += 0
    else:
        raise AssertionError('_match result should by in either wins, ties or losses. Encoding is probably incorrect.')
    score += shapePoints[_match[-1]]
    return score


# convert A, B, C to R, P S and X Y Z to R P S as well
# convertion how you first thought it was meant
def convertToRPSWrong(_match):
    return _match.replace('\n', '').replace('A', 'R').replace('B', 'P').replace('C', 'S')\
        .replace('X', 'R').replace('Y', 'P').replace('Z', 'S')


# second method: X Y Z means lose, tie, win
def convertToRPSRight(_match):
    _match = _match.replace('\n', '').replace('A', 'R').replace('B', 'P').replace('C', 'S')
    if _match[-1] == 'X':
        return _match[0] + ' ' + loseDict[_match[0]]
    elif _match[-1] == 'Y':
        return _match[0] + ' ' + tieDict[_match[0]]
    elif _match[-1] == 'Z':
        return _match[0] + ' ' + winDict[_match[0]]
    else:
        raise AssertionError('No valid last character in match. It should be X, Y or Z')


with open('input.txt') as f:
    lines = f.readlines()

# trim \n from output and parse to standard encoding
matchStrategyWrong = [convertToRPSWrong(line) for line in lines]
matchStrategyRight = [convertToRPSRight(line) for line in lines]

strategyScoreWrong = 0
for match in matchStrategyWrong:
    strategyScoreWrong += countScore(match)

strategyScoreRight = 0
for match in matchStrategyRight:
    strategyScoreRight += countScore(match)

print(strategyScoreWrong)
print(strategyScoreRight)
