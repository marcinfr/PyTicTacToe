class ResultChecker:
    def __init__(self):
        self.winningRow = [0,0]

    def isWinningMove(self, game, lastMove, player = False):
        if (player == False):
            player = game.currentPlayer
        if self.isWinningLine(game, lastMove, [1, 0], player):
            return True
        if self.isWinningLine(game, lastMove, [0, 1], player):
            return True
        if self.isWinningLine(game, lastMove, [1, 1], player):
            return True
        if self.isWinningLine(game, lastMove, [1, -1], player):
            return True
        return False

    def isWinningLine(self, game, lastMove, vector, player):
        sameInRow = 0
        isLastMoveDone = not game.board[lastMove[0]][lastMove[1]] == 0
        linesToWin = game.linesToWin
        if not isLastMoveDone:
            linesToWin -= 1
        for i in range(-game.linesToWin, game.linesToWin):
            x = lastMove[0] - (vector[0] * i) 
            y = lastMove[1] + (vector[1] * i)
            if (x >= 0 and y >= 0 and x < game.boardSize and y < game.boardSize and game.board[x][y] == player):
                if sameInRow == 0:
                    self.winningRow[0] = [x,y]
                sameInRow = sameInRow + 1
                if sameInRow >= linesToWin:
                    self.winningRow[1] = [x,y]
                    return True
            else:
                if (x != lastMove[0] or y != lastMove[1]):
                    sameInRow = 0
        return False