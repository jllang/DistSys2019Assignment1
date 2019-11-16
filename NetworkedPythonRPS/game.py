import enum

class Play(enum.Enum):
    Rock     = 1
    Paper    = 2
    Scissors = 3
    Timeout  = 4

class Outcome(enum.Enum):
    Win          = 1
    Tie          = 2
    Lose         = 3
    Inconclusive = 4

class Game:
    def __init__(self, id):
        self.ready    = False
        self.id       = id
        self.played   = (False, False, False)
        self.plays    = (Timeout, Timeout, Timeout)
        self.score    = (0, 0, 0)
        self.outcomes = (Tie, Tie, Tie)

    def get_player_move(self, p):
        return self.plays[p]

    def play(self, player, move):
        self.plays[player] = move
        self.played[player] = True

    def connected(self):
        return self.ready

    def everyonePlayed(self):
        return self.played[0] and self.played[1] and self.played[2]

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
        compare(self, 0, 1, s)
        compare(self, 0, 2, s)
        compare(self, 1, 2, s)
        if s[0] == s[1] and s[1] == s[2]:
            if s[0] == 0 and self.plays[0] != Play.Timeout:
                print("The round ends in a tie between all players.")
                o = (Tie, Tie, Tie)
            else:
                print("The round ends inconclusively.")
                s = (0, 0, 0)
                o = (Inconclusive, Inconclusive, Inconclusive)
        elif    (s[0] > s[1] and s[1] >= s[2]) \
             or (s[0] > s[2] and s[2] >= s[1]):
            print("Player 1 wins the round")
            o = (Win, Lose, Lose)
        elif    (s[1] > s[0] and s[0] >= s[2]) \
             or (s[1] > s[2] and s[2] >= s[0]):
            print("Player 2 wins the round")
            o = (Lose, Win, Lose)
        elif    (s[2] > s[0] and s[0] >= s[1]) \
             or (s[2] > s[1] and s[1] >= s[0]):
            print("Player 3 wins the round")
            o = (Lose, Lose, Win)
        elif s[0] == s[1] and s[1] >= s[2]:
            print("Player 3 loses the round")
            o = (Tie, Tie, Lose)
        elif s[1] == s[2] and s[2] >= s[0]:
            print("Player 1 loses the round")
            o = (Lose, Tie, Tie)
        elif s[0] == s[2] and s[2] >= s[1]:
            print("Player 2 loses the round")
            o = (Tie, Lose, Tie)
        self.scores[0] += s[0]
        self.scores[1] += s[1]
        self.scores[2] += s[2]
        self.outcomes = o
