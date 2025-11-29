import random
import time

class Random:
    def __init__(self, name, game, wait = 0):
        self.name = name
        self.game = game
        self.wait = wait
        self.startRound = False

    def getMove(self, events):
        current_time = time.time()

        if (self.startRound == False):
            self.startRound = current_time

        if (current_time - self.startRound > self.wait):
            return [
                random.randint(0, self.game.boardSize - 1),
                random.randint(0, self.game.boardSize - 1)
            ]
        return False

    def endMove(self):
        self.startRound = False