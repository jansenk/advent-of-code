DAY_NUM = 2
from enum import Enum
from ..utils import iterlines

class Result(Enum):
    WIN = 6
    LOSE = 0
    DRAW = 3
    
    @staticmethod
    def parse(s):
        if s == 'X':
            return Result.LOSE
        elif s == 'Y':
            return Result.DRAW
        else:
            return Result.WIN

class Hand(Enum):
    ROCK = 1
    PAPER = 2
    SCISSORS = 3

    @staticmethod
    def parse(s):
        if s in ('A', 'X'):
            return Hand.ROCK
        elif s in ('B', 'Y'):
            return Hand.PAPER
        else:
            return Hand.SCISSORS
    
    def fight(self, other):
        if self == other:
            return Result.DRAW
    
        if self == Hand.ROCK and other == Hand.PAPER:
            return Result.LOSE
        if self == Hand.PAPER and other == Hand.SCISSORS:
            return Result.LOSE
        if self == Hand.SCISSORS and other == Hand.ROCK:
            return Result.LOSE

        return Result.WIN            

def part1(is_test):
    total_score = 0
    for line in iterlines(2, is_test):
        line = line.split()
        opponent = Hand.parse(line[0])
        player = Hand.parse(line[1])
        result = player.fight(opponent)
        total_score += result.value + player.value
    print(total_score)

def part2(is_test):
    total_score = 0
    for line in iterlines(2, is_test):
        line = line.split()
        opponent = Hand.parse(line[0])
        result = Result.parse(line[1])
        for player in (Hand.ROCK, Hand.SCISSORS, Hand.PAPER):
            if player.fight(opponent) == result:
                total_score += result.value + player.value
    print(total_score)


def tests():
    assert Hand.ROCK.fight(Hand.SCISSORS) == Result.WIN
    assert Hand.ROCK.fight(Hand.PAPER) == Result.LOSE
    assert Hand.ROCK.fight(Hand.ROCK) == Result.DRAW
    
    assert Hand.PAPER.fight(Hand.ROCK) == Result.WIN
    assert Hand.PAPER.fight(Hand.SCISSORS) == Result.LOSE
    assert Hand.PAPER.fight(Hand.PAPER) == Result.DRAW

    assert Hand.SCISSORS.fight(Hand.PAPER) == Result.WIN
    assert Hand.SCISSORS.fight(Hand.ROCK) == Result.LOSE
    assert Hand.SCISSORS.fight(Hand.SCISSORS) == Result.DRAW

tests()
part1(True)
part1(False)

part2(True)
part2(False)

            
