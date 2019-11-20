from enum import Enum, unique

@unique
class Play(Enum):
    Rock     = 1
    Paper    = 2
    Scissors = 3
    Timeout  = 4

def stringToPlay(str):
    if str == "Rock":
        return Play.Rock
    elif str == "Paper":
        return Play.Paper
    elif str == "Scissors":
        return Play.Scissors
    else:
        return "Timeout"

@unique
class Outcome(Enum):
    Win          = 1
    Tie          = 2
    Lose         = 3
    Inconclusive = 4

def stringToOutcome(str):
    if str == "Win":
        return Outcome.Win
    elif str == "Tie":
        return Outcome.Tie
    elif str == "Lose":
        return Outcome.Lose
    else:
        return "Inconclusive"

class Game:
    def __init__(self, id):
        self.ready    = False
        self.id       = id
        self.played   = (False, False, False)
        self.plays    = (Play.Timeout, Play.Timeout, Play.Timeout)
        self.score    = (0, 0, 0)
        self.outcomes = (Outcome.Tie, Outcome.Tie, Outcome.Tie)

    def get_player_move(self, p):
        return self.plays[p]

    def play(self, player, move):
        self.plays[player]  = move
        self.played[player] = True

    def connected(self):
        return self.ready

    def everyonePlayed(self):
        return self.played[0] and self.played[1] and self.played[2]

    def resetPlayed(self):
        self.played = (False, False, False)

    # Assigns score to players a and b.
    def compare(self, a, b, s):
        ma = self.plays[a]
        mb = self.plays[b]
        if ma != mb:
            if ma == Play.Rock:
                if mb == Play.Paper:
                    s[b] += 1
                else:
                    s[a] += 1
            elif ma == Play.Paper:
                if mb == Play.Rock:
                    s[a] += 1
                else:
                    s[b] += 1
            else:
                if plays[b] == Play.Paper:
                    s[a] += 1
                else:
                    s[b] += 1

    #Judges the outcome of a round of the game.
    def judge(self):
        s = (0, 0, 0)
        o = (Outcome.Inconclusive, Outcome.Inconclusive, Outcome.Inconclusive)
        compare(self, 0, 1, s)
        compare(self, 0, 2, s)
        compare(self, 1, 2, s)
        if s[0] == s[1] and s[1] == s[2]:
            if s[0] == 0 and self.plays[0] != Play.Timeout:
                print("The round ends in a tie between all players.")
                o = (Outcome.Tie, Outcome.Tie, Outcome.Tie)
            else:
                print("The round ends inconclusively.")
                s = (0, 0, 0)
        elif    (s[0] > s[1] and s[1] >= s[2]) \
             or (s[0] > s[2] and s[2] >= s[1]):
            print("Player 1 wins the round")
            o = (Outcome.Win, Outcome.Lose, Outcome.Lose)
        elif    (s[1] > s[0] and s[0] >= s[2]) \
             or (s[1] > s[2] and s[2] >= s[0]):
            print("Player 2 wins the round")
            o = (Outcome.Lose, Outcome.Win, Outcome.Lose)
        elif    (s[2] > s[0] and s[0] >= s[1]) \
             or (s[2] > s[1] and s[1] >= s[0]):
            print("Player 3 wins the round")
            o = (Outcome.Lose, Outcome.Lose, Outcome.Win)
        elif s[0] == s[1] and s[1] >= s[2]:
            print("Player 3 loses the round")
            o = (Outcome.Tie, Outcome.Tie, Outcome.Lose)
        elif s[1] == s[2] and s[2] >= s[0]:
            print("Player 1 loses the round")
            o = (Outcome.Lose, Outcome.Tie, Outcome.Tie)
        elif s[0] == s[2] and s[2] >= s[1]:
            print("Player 2 loses the round")
            o = (Outcome.Tie, Outcome.Lose, Outcome.Tie)
        self.scores[0] += s[0]
        self.scores[1] += s[1]
        self.scores[2] += s[2]
        self.outcomes = o
