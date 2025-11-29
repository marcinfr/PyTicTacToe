from helpers.resultChecker import ResultChecker

class Game:
    def __init__(self, boardSize=3, linesToWin=3):
        self.boardSize = boardSize
        self.linesToWin = linesToWin
        self.players = []
        self.resultChecker = ResultChecker();
        self.resetGame()

    def resetGame(self):
        self.board = [[0 for _ in range(self.boardSize)] for _ in range(self.boardSize)]
        self.currentPlayer = -1
        self.isRunning = 1
        self.winner = 0
        self.emptyCellsQty = self.boardSize * self.boardSize

    def addPlayer(self, player):
        self.players.append(player)

    def getCurrentPlayer(self):
        return self.players[int((self.currentPlayer + 2) / 2)]

    def run(self, events = False):
        if (not self.isRunning):
            return
        
        move = self.getCurrentPlayer().getMove(events);
        if (move and self.board[move[0]][move[1]] == 0):
            self.board[move[0]][move[1]] = self.currentPlayer
            self.getCurrentPlayer().endMove()
            if (self.resultChecker.isWinningMove(self, move)):
                self.isRunning = False
                self.winner = self.currentPlayer
                return
            if (self.emptyCellsQty == 0):
                self.isRunning = 0
                return
            self.nextPlayer()

    def nextPlayer(self):
        self.currentPlayer = (-1) * self.currentPlayer
        