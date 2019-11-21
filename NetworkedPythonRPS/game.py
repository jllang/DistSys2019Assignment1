class Game:
    def __init__(self, id):
        # initially player 1's move is false
        self.p1Went = False
        # initially player 2's move is false
        self.p2Went = False
        self.ready = False
        # current game's id
        self.id = id
        # two players move, initially none[player1's move, player2's move]
        self.moves = [None, None]
        # initially palyer1 and player2 both 0
        self.wins = [0,0]
        # if ties
        self.ties = 0

    # get the player's move, either player 1's move or player 2's move
    def get_player_move(self, p):

        return self.moves[p]

    # updates the moves list with that certain player's move
    def play(self, player, move):
        self.moves[player] = move
        # for player 1, if player1 makes a move then p1 went is true that means p1 already made a move
        if player == 0:
            self.p1Went = True
        else:
            self.p2Went = True

    # check if the two player's connected to the game or not
    def connected(self):
        return self.ready

    # check if both of the player made a move or not
    def bothWent(self):
        return self.p1Went and self.p2Went

    # deciding the winner
    def winner(self):
        # taking only the first letter of the move(R from Rock)
        p1 = self.moves[0].upper()[0]
        p2 = self.moves[1].upper()[0]

        winner = -1
        if p1 == "R" and p2 == "S":
            winner = 0
        elif p1 == "S" and p2 == "R":
            winner = 1
        elif p1 == "P" and p2 == "R":
            winner = 0
        elif p1 == "R" and p2 == "P":
            winner = 1
        elif p1 == "S" and p2 == "P":
            winner = 0
        elif p1 == "P" and p2 == "S":
            winner = 1

        return winner

    # after the game we reset the state of the players
    def resetWent(self):
        self.p1Went = False
        self.p2Went = False