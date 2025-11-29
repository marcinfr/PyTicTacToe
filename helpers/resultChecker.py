class ResultChecker:
    def __init__(self):
        self.winningRow = [0,0]

    def checkResult(self, game, lastMove):
        if game.isRunning:
            self.checkLine(game, lastMove, [1, 0])
        if game.isRunning:
            self.checkLine(game, lastMove, [0, 1])
        if game.isRunning:
            self.checkLine(game, lastMove, [1, 1])
        if game.isRunning:
            self.checkLine(game, lastMove, [1, -1])
        if not game.isRunning:
            print("koniec!!");
            print(self.winningRow)

    def checkLine(self, game, lastMove, vector):
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
                    game.isRunning = False
            else:
                sameInRow = 0
