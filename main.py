import pygame
import sys
import math
from game import Game
from players.human import Human
from players.random import Random
from screen.button import Button
from helpers.events import Events

class TicTacToe:
    def __init__(self, cellSize = 150):
        self.game = Game(3, 3)
        self.cellSize = cellSize
        self.boardWidth = self.game.boardSize * cellSize
        self.windowWidth = self.boardWidth
        self.boardHeight = self.game.boardSize * cellSize
        self.windowHeight = self.boardHeight + 60
        self.menu = 1
        self.events = Events()
        pygame.init()
        pygame.display.set_caption("Tic Tac Toe")
        self.screen = pygame.display.set_mode(
            (
                self.windowWidth,
                self.windowHeight
            )
        )

    def printBoard(self):
        posX, posY = pygame.mouse.get_pos()
        cellWithCursor = self.getCellByPosition(posX, posY)
        if cellWithCursor != False and self.game.board[cellWithCursor[0]][cellWithCursor[1]] == 0:
            if self.game.currentPlayer < 0:
                self.printX(cellWithCursor[0], cellWithCursor[1], (205,205,205));
            else:
                self.printO(cellWithCursor[0], cellWithCursor[1], (205,205,205));
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

    def getCellByPosition(self, posX, posY, onlyAvailable = True):
        x = int(posX / self.cellSize);
        if x < 0:
            return False
        if x > self.game.boardSize:
            return False
        y = int(posY / self.cellSize);
        if onlyAvailable and (x < 0 or x >= self.game.boardSize):
            return False
        if onlyAvailable and (y < 0 or y >= self.game.boardSize):
            return False
        return [x, y]
    
    def printMenu(self):
        font = pygame.font.Font(None, 170) 
        text = font.render("TIC", True, "white")
        textRect = text.get_rect()
        centerX = self.windowWidth / 2
        centerY = 100
        textRect.center = (centerX, centerY)
        self.screen.blit(text, textRect)
        
        text = font.render("TAC", True, "white")
        centerY = 190
        textRect = text.get_rect()
        textRect.center = (centerX, centerY)
        self.screen.blit(text, textRect)

        text = font.render("TOE", True, "white")
        centerY = 280
        textRect = text.get_rect()
        textRect.center = (centerX, centerY)
        self.screen.blit(text, textRect)

        startButton = Button(self.windowWidth / 2 - 100, 330, 200, 40, "Start")
        startButton.setOnclick(self.startGame)
        startButton.display(self.screen, self.events)
        exitButton = Button(self.windowWidth / 2 - 100, 380, 200, 40, "Exit")
        exitButton.setOnclick(self.exit)
        exitButton.setHoverBackgroudColor("red")
        exitButton.display(self.screen, self.events)

    def printGame(self):
        self.printBoard()
        boardY = self.cellSize * self.game.boardSize;
        endButton = Button(self.windowWidth - 110, boardY + 10, 100, 40, "Exit")
        endButton.setOnclick(self.stopGame)
        endButton.setHoverBackgroudColor("red")
        endButton.display(self.screen, self.events)

    def startGame(self):
        self.menu = 0

    def stopGame(self):
        self.menu = 1
        self.game.resetGame()

    def exit(self):
        pygame.quit()
        sys.exit()

    def displayBackgroud(self):
        self.screen.fill("lightgrey")
        if self.menu == 1:
            posX, posY = pygame.mouse.get_pos()
            cell = self.getCellByPosition(posX, posY, False)
            for x in range(0, self.game.boardSize):
                for y in range(0, self.game.boardSize + 1):
                    if (cell != False and x == cell[0] and y == cell[1]):
                       isMouseOver = True
                    else:
                        isMouseOver = False
                    if ((x + y) % 2 == 0):
                        color = (205,205,205)
                        if isMouseOver:
                            color = color = (190,190,220)
                        self.printO(x , y, color)
                    else:
                        color = (205,205,205)
                        if isMouseOver:
                            color = color = (220,190,190)
                        self.printX(x , y, color)

    def run(self):
        print("Run")
        while True:
            self.events.reset();
            if self.events.QUIT:
                self.exit()

            self.displayBackgroud()

            if self.menu == 1:
                self.printMenu()
            else:
                self.game.run(self.events)
                self.printGame()
            pygame.display.flip()

ticTacToe = TicTacToe()
player1 = Human("Player Blue", ticTacToe)
player2 = Human("Player Red", ticTacToe)
#player2 = Random("Random", ticTacToe.game, 1)
ticTacToe.game.addPlayer(player1)
ticTacToe.game.addPlayer(player2)
ticTacToe.run()