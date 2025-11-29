class ResultChecker:
    def __init__(self):
        self.winningRow = [0,0]

    def isWinningMove(self, game, lastMove):
        if self.isWinningLine(game, lastMove, [1, 0]):
            return True
        if self.isWinningLine(game, lastMove, [0, 1]):
            return True
        if self.isWinningLine(game, lastMove, [1, 1]):
            return True
        if self.isWinningLine(game, lastMove, [1, -1]):
            return True
        return False

    def isWinningLine(self, game, lastMove, vector):
        sameInRow = 0
        for i in range(-game.linesToWin, game.linesToWin):
            x = lastMove[0] - (vector[0] * i) 
            y = lastMove[1] + (vector[1] * i)
            if (x >= 0 and y >= 0 and x < game.boardSize and y < game.boardSize and game.board[x][y] == game.currentPlayer):
                if sameInRow == 0:
                    self.winningRow[0] = [x,y]
                sameInRow = sameInRow + 1
                if sameInRow >= game.linesToWin:
                    self.winningRow[1] = [x,y]
                    return True
            else:
                sameInRow = 0
        return False