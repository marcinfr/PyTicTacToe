import random
import time

class Random:
    def __init__(self, name, game):
        self.name = name
        self.game = game
        self.wait = 0
        self.startRound = False

    def getMove(self, events = False):
        if (self.wait > 0):
            current_time = time.time()
            if (self.startRound == False):
                self.startRound = current_time

        if (self.wait == 0 or current_time - self.startRound > self.wait):
            emptyCells = []
            for x in range(0, self.game.boardSize):
                for y in range(0, self.game.boardSize):
                    if (self.game.board[x][y] == 0):
                        if random.random() < 0.9:
                            if (self.game.resultChecker.isWinningMove(self.game, [x, y], 1)):
                                return [x, y]
                            if (self.game.resultChecker.isWinningMove(self.game, [x, y], -1)):
                                return [x, y]
                        emptyCells.append([x, y])
            cell = random.choice(emptyCells)
            return cell
        return False
    
    def setWait(self, wait):
        self.wait = wait

    def endMove(self):
        self.startRound = False