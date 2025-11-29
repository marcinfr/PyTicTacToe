import pygame

class Human:
    def __init__(self, name, ticTacToe):
        self.name = name
        self.move = False
        self.ticTacToe = ticTacToe

    def getMove(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = event.pos
                self.move = self.ticTacToe.getCellByPosition(pos[0], pos[1])
        return self.move
    
    def endMove(self):
        self.move = False