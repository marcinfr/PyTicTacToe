from helpers.resultChecker import ResultChecker

class Game:
    def __init__(self, boardSize=3, linesToWin=3):
        print("Init Game")
        self.boardSize = boardSize
        self.linesToWin = linesToWin
        self.players = []
        self.resultChecker = ResultChecker();
        self.resetGame()

    def resetGame(self):
        self.board = self.array = [[0 for _ in range(self.boardSize)] for _ in range(self.boardSize)]
        self.currentPlayer = -1
        self.isRunning = 1

    def addPlayer(self, player):
        self.players.append(player)

    def getCurrentPlayer(self):
        return self.players[int((self.currentPlayer + 2) / 2)]

    def run(self, events):
        if (not self.isRunning):
            return
        
        move = self.getCurrentPlayer().getMove(events);
        if (move and self.board[move[0]][move[1]] == 0):
            self.board[move[0]][move[1]] = self.currentPlayer
            self.resultChecker.checkResult(self, move)
            self.nextPlayer()

    def nextPlayer(self):
        self.getCurrentPlayer().endMove()
        self.currentPlayer = (-1) * self.currentPlayer
        