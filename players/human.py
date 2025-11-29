import pygame

class Human:
    def __init__(self, name, ticTacToe):
        self.name = name
        self.move = False
        self.ticTacToe = ticTacToe

    def getMove(self, events):
        if events.MOUSEBUTTONDOWN:
            pos = events.EVENTPOSITION
            self.move = self.ticTacToe.getCellByPosition(pos[0], pos[1])
        return self.move
    
    def endMove(self):
        self.move = False