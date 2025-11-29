import pygame
import sys
from game import Game
from players.human import Human
from players.random import Random

class TicTacToe:
    def __init__(self, cellSize = 80):
        self.game = Game(8, 3);
        self.cellSize = cellSize;
        pygame.init()
        pygame.display.set_caption("Tic Tac Toe")
        self.screen = pygame.display.set_mode(
            (
                self.game.boardSize * cellSize, 
                self.game.boardSize * cellSize
            )
        )

    def printBoard(self):
        pygame.display.flip()
        self.screen.fill("lightgrey")
        posX, posY = pygame.mouse.get_pos()
        cellWithCursor = self.getCellByPosition(posX, posY)
        if cellWithCursor != False:
            pygame.draw.rect(self.screen, "grey", (
                cellWithCursor[0] * self.cellSize,
                cellWithCursor[1] * self.cellSize,
                self.cellSize,
                self.cellSize,
            ))
        for x in range(0, self.game.boardSize):
            pygame.draw.line(
                self.screen, 
                "white", 
                ((x + 1) * self.cellSize, 0), 
                ((x + 1) * self.cellSize, self.cellSize * self.game.boardSize)
            )
            pygame.draw.line(
                self.screen, 
                "white", 
                (0, (x + 1) * self.cellSize), 
                (self.cellSize * self.game.boardSize, (x + 1) * self.cellSize)
            )
            for y in range(0, self.game.boardSize):
                if (self.game.board[x][y] < 0):
                    self.printX(x, y)
                if (self.game.board[x][y] > 0):
                    self.printO(x, y)
        if (not self.game.isRunning):
            winnigLine = self.game.resultChecker.winningRow
            pygame.draw.line(
                self.screen, 
                "black", 
                (winnigLine[0][0] * self.cellSize + self.cellSize / 2, winnigLine[0][1] * self.cellSize + self.cellSize / 2),  
                (winnigLine[1][0] * self.cellSize + self.cellSize / 2, winnigLine[1][1] * self.cellSize + self.cellSize / 2),  
                int(self.cellSize * 0.1)
            )

    def printX(self, x , y, color = "red"):
        margin = self.cellSize * 0.2
        pygame.draw.line(
            self.screen,
            color, 
            (x * self.cellSize + margin, y * self.cellSize + margin), 
            ((x + 1) * self.cellSize - margin, (y + 1) * self.cellSize - margin), 
            int(self.cellSize * 0.2)
        )
        pygame.draw.line(
            self.screen,
            color, 
            ((x + 1) * self.cellSize - margin, y * self.cellSize + margin), 
            (x * self.cellSize + margin, (y + 1) * self.cellSize - margin), 
            int(self.cellSize * 0.2)
        )

    def printO(self, x, y, color = "blue"):
        pygame.draw.circle(
            self.screen, 
            color, 
            (x * self.cellSize + self.cellSize / 2, y * self.cellSize + self.cellSize / 2), 
            self.cellSize / 2 * 0.7,
            int(self.cellSize * 0.2)
        )

    def getCellByPosition(self, posX, posY):
        x = int(posX / self.cellSize);
        if x < 0:
            return False
        if x > self.game.boardSize:
            return False
        y = int(posY / self.cellSize);
        if y < 0:
            return False
        if y > self.game.boardSize:
            return False
        return [x, y]

    def run(self):
        print("Run")
        while True:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            self.game.run(events)
            self.printBoard()

ticTacToe = TicTacToe()
player1 = Human("Player Blue", ticTacToe)
player2 = Human("Player Red", ticTacToe)
#player2 = Random("Random", ticTacToe.game, 1)
ticTacToe.game.addPlayer(player1)
ticTacToe.game.addPlayer(player2)
ticTacToe.run()