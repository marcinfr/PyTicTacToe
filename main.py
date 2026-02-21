import pygame
import sys
import math
import os
from game import Game
from players.human import Human
from players.random import Random
from players.ai import AiPlayer
from players.aiMonteCarlo import AiMonteCarlo
from screen.button import Button
from helpers.events import Events
from aiTrainer import AiTrainer
import random

class TicTacToe:
    STATE_MENU = 0
    STATE_GAME = 1
    STATE_TAINING = 2

    MENU_MAIN = "main"
    MENU_GAME_OPTIONS = "gameOptions"

    BOARDS = [
        {
            "size": (3, 3),
            "winLength": 3,
            "varnishingElementsLimit": 3,
        },
        {
            "size": (5, 5),
            "winLength": 4,
            "varnishingElementsLimit": 5,
        },
        {
            "size": (10, 10),
            "winLength": 5,
            "varnishingElementsLimit": 7,
        },
    ]

    MODES = [
        {
            "code": Game.MODE_CLASSIC,
            "label": 'Classic',
        },
        {
            "code": Game.MODE_VARNISHING,
            "label": 'Varnishing',
        }
    ]

    TIMES = [
        0,
        3,
        5,
        10,
    ]

    def __init__(self):
        self.currentBoard = 0;
        self.currentMode = 0;
        self.timeOption = 0;
        self.currentMenu = self.MENU_MAIN;
        is_steam_deck = os.environ.get("SteamDeck") == "1"

        #self.cellSize = cellSize
        #self.boardWidth = self.game.boardSize * cellSize
        #self.windowWidth = self.boardWidth
        #self.boardHeight = self.game.boardSize * cellSize
        #self.windowHeight = self.boardHeight + 60


        self.gameState = self.STATE_MENU
        self.events = Events()
        pygame.init()
        pygame.display.set_caption("Tic Tac Toe")
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

        if is_steam_deck:
            pygame.mouse.set_visible(False)

        #self.screen = pygame.display.set_mode((1280, 800))
        self.windowWidth, self.windowHeight = self.screen.get_size()
        self.boardHeight = self.windowHeight - 40
        self.boardWidth = self.windowWidth
        self.initGame()

    def printBoard(self):
        posX, posY = pygame.mouse.get_pos()
        cellWithCursor = self.getCellByPosition(posX, posY)
        if cellWithCursor != False and self.game.board[cellWithCursor[0]][cellWithCursor[1]] == 0:
            if self.game.currentPlayer < 0:
                self.printX(cellWithCursor[0], cellWithCursor[1], (205,205,205));
            else:
                self.printO(cellWithCursor[0], cellWithCursor[1], (205,205,205));
        
        pygame.draw.line(
            self.screen, 
            "white", 
            (self.marginX, self.marginY), 
            (self.marginX, self.cellSize * self.game.boardSize[1] + self.marginY)
        )
        
        pygame.draw.line(
            self.screen, 
            "white", 
            (self.marginX, self.marginY), 
            (self.cellSize * self.game.boardSize[0] + self.marginX, self.marginY)
        )

        for y in range(0, self.game.boardSize[1]):
            pygame.draw.line(
                self.screen, 
                "white", 
                (self.marginX, (y + 1) * self.cellSize + self.marginY), 
                (self.cellSize * self.game.boardSize[0] + self.marginX, (y + 1) * self.cellSize + self.marginY)
            )

        moveToVarnishing = self.game.getMoveToVarnishing()

        for x in range(0, self.game.boardSize[0]):
            pygame.draw.line(
                self.screen, 
                "white", 
                ((x + 1) * self.cellSize + self.marginX, self.marginY), 
                ((x + 1) * self.cellSize + self.marginX, self.cellSize * self.game.boardSize[1] + self.marginY  )
            )
            for y in range(0, self.game.boardSize[1]):
                color = False
                if moveToVarnishing == (x,y):
                    color = "grey"
                if (self.game.board[x][y] < 0):
                    if not color:
                        color = "red"
                    self.printX(x, y, color)
                if (self.game.board[x][y] > 0):
                    if not color:
                        color = "blue"
                    self.printO(x, y, color)
        if (not self.game.isRunning and self.game.winner != 0):
            winnigLine = self.game.resultChecker.winningRow
            pygame.draw.line(
                self.screen, 
                "black", 
                (winnigLine[0][0] * self.cellSize + self.cellSize / 2 + self.marginX, winnigLine[0][1] * self.cellSize + self.cellSize / 2 + self.marginY),  
                (winnigLine[1][0] * self.cellSize + self.cellSize / 2 + self.marginX, winnigLine[1][1] * self.cellSize + self.cellSize / 2 + self.marginY),  
                int(self.cellSize * 0.1)
            )

    def printX(self, x , y, color = "red"):
        margin = self.cellSize * 0.2
        pygame.draw.line(
            self.screen,
            color, 
            (x * self.cellSize + margin + self.marginX, y * self.cellSize + margin + self.marginY), 
            ((x + 1) * self.cellSize - margin + self.marginX, (y + 1) * self.cellSize - margin + self.marginY), 
            int(self.cellSize * 0.2)
        )
        pygame.draw.line(
            self.screen,
            color, 
            ((x + 1) * self.cellSize - margin + self.marginX, y * self.cellSize + margin + self.marginY), 
            (x * self.cellSize + margin + self.marginX, (y + 1) * self.cellSize - margin + self.marginY), 
            int(self.cellSize * 0.2)
        )

    def printO(self, x, y, color = "blue"):
        pygame.draw.circle(
            self.screen, 
            color, 
            (x * self.cellSize + self.cellSize / 2 + self.marginX, y * self.cellSize + self.cellSize / 2 + self.marginY), 
            self.cellSize / 2 * 0.7,
            int(self.cellSize * 0.2)
        )

    def getCellByPosition(self, posX, posY, onlyAvailable = True):
        x = int((posX - self.marginX) / self.cellSize);
        if x < 0:
            return False
        if x > self.game.boardSize[0]:
            return False
        y = int((posY - self.marginY) / self.cellSize);
        if onlyAvailable and (x < 0 or x >= self.game.boardSize[0]):
            return False
        if onlyAvailable and (y < 0 or y >= self.game.boardSize[1]):
            return False
        return [x, y]
    
    def printMenu(self):
        if self.currentMenu == self.MENU_MAIN:
            font = pygame.font.Font(None, 240) 
            menuY = 450
            letterSpacing = 140
        else:
            font = pygame.font.Font(None, 140) 
            letterSpacing = 80
            menuY = 300

        text = font.render("TIC", True, "white")
        textRect = text.get_rect()
        centerX = self.windowWidth / 2
        centerY = 100
        textRect.center = (centerX, centerY)
        self.screen.blit(text, textRect)
        
        text = font.render("TAC", True, "white")
        centerY = 100 + letterSpacing
        textRect = text.get_rect()
        textRect.center = (centerX, centerY)
        self.screen.blit(text, textRect)

        text = font.render("TOE", True, "white")
        centerY = 100 + letterSpacing * 2
        textRect = text.get_rect()
        textRect.center = (centerX, centerY)
        self.screen.blit(text, textRect)

        currentBoard = self.BOARDS[self.currentBoard]
        inRow = str(currentBoard["winLength"])

        boardLabel = str(currentBoard["size"][0]) + "x" + str(currentBoard["size"][1]) + ", " + inRow + " in row to win"
        modeLabel = self.MODES[self.currentMode]['label']

        timePerMove = self.TIMES[self.timeOption]
        timeLabel = "Time: " + (str(timePerMove) + "s" if timePerMove > 0 else "No time limit")

        buttons = {
            self.MENU_MAIN: [
                {
                    "text": "New Game",
                    "onclick": [self.openMenu, self.MENU_GAME_OPTIONS],
                    "hoverBackgroundColor": "darkgreen",
                },
                # {
                #     "text": "Train AI",
                #     "onclick": self.trainAi,
                #     "hoverBackgroundColor": "darkgreen",
                # }
                {
                    "text": "Exit",
                    "onclick": self.exit,
                    "hoverBackgroundColor": "red",
                }
            ],
            self.MENU_GAME_OPTIONS: [
                {
                    "text": "Start Game",
                    "onclick": self.startGame,
                    "hoverBackgroundColor": "darkgreen",
                },
                               {
                    "text": boardLabel,
                    "onclick": self.nextBoard,
                },
                {
                    "text": modeLabel,
                    "onclick": self.nextMode,
                },
                {
                    "text": timeLabel,
                    "onclick": self.nextTime,
                },
                {
                    "text": "Back",
                    "onclick": [self.openMenu, self.MENU_MAIN],
                    "hoverBackgroundColor": "red",
                }
            ]
        }

        buttonHeight = 80
        for buttonData in buttons[self.currentMenu]:
            button = Button(self.windowWidth / 2 - 150, menuY, 300, buttonHeight, buttonData["text"])
            button.setOnclick(buttonData["onclick"])
            if "hoverBackgroundColor" in buttonData:
                button.setHoverBackgroudColor(buttonData["hoverBackgroundColor"])
            button.display(self.screen, self.events)
            menuY += buttonHeight + 10
        return

        #startButton = Button(self.windowWidth / 2 - 150, 380, 300, 80, "Start")
        #startButton.setOnclick(self.startGame)
        #startButton.setHoverBackgroudColor("darkgreen")
        #startButton.display(self.screen, self.events)

        #label = "Train AI"
        #if (self.gameState == self.STATE_TAINING):
        #    label = "Stop Training"
        #trainAiButton = Button(self.windowWidth / 2 - 100, 380, 200, 40, label)
        #if (self.gameState == self.STATE_TAINING):
        #    trainAiButton.setOnclick(self.stopTrainAi)
        #    trainAiButton.setHoverBackgroudColor("red")
        #else:
        #    trainAiButton.setOnclick(self.trainAi)
        #trainAiButton.display(self.screen, self.events)


    def openMenu(self, menu):
        self.currentMenu = menu

    def nextBoard(self):
        self.currentBoard += 1
        if self.currentBoard >= len(self.BOARDS):
            self.currentBoard = 0
        self.initGame()

    def nextMode(self):
        self.currentMode += 1
        if self.currentMode >= len(self.MODES):
            self.currentMode = 0

    def nextTime(self):
        self.timeOption += 1
        if self.timeOption >= len(self.TIMES):
            self.timeOption = 0

    def printGame(self):
        self.printBoard()
        boardX = self.cellSize * self.game.boardSize[0];
        boardY = self.cellSize * self.game.boardSize[1];

        if self.game.timeLimit > 0:
            font = pygame.font.Font(None, 40) 
            text = font.render("Time left", True, "darkgrey")
            textRect = text.get_rect()
            textRect.center = self.marginX + boardX + self.marginX / 2, 40
            self.screen.blit(text, textRect)
            if self.game.timePerMoveInSeconds <= 3:
                timeColor = "red"
                fontSize = 60
            else:                
                timeColor = "darkgrey"
                fontSize = 60

            font = pygame.font.Font(None, fontSize)
            timeLeft = str(self.game.timePerMoveInSeconds)

            timeText = font.render(timeLeft + "s", True, timeColor)
            timeTextRect = timeText.get_rect()
            timeTextRect.center = self.marginX + boardX + self.marginX / 2, 80
            self.screen.blit(timeText, timeTextRect)

        #exitButton = Button(self.windowWidth / 2 - 150, 650, 300, 80, "Exit")
        buttonWidth = self.screen.get_size()[0] / 2 - boardY / 2 - self.marginY * 2

        if (not self.game.isRunning):
            playAgainButton = Button(
                self.marginX + boardX+ self.marginY, 
                self.screen.get_size()[1] - self.marginY - 170,
                buttonWidth,
                80,
                "Play Again"
            )
            playAgainButton.setOnclick(self.startGame)
            playAgainButton.setHoverBackgroudColor("darkgreen")
            playAgainButton.display(self.screen, self.events)

        endButton = Button(
            self.marginX + boardX+ self.marginY, 
            self.screen.get_size()[1] - self.marginY - 80,
            buttonWidth,
            80,
            "Exit"
        )
        endButton.setOnclick(self.stopGame)
        endButton.setHoverBackgroudColor("red")
        endButton.display(self.screen, self.events)

    def initGame(self):
        board = self.BOARDS[self.currentBoard]
        mode = self.MODES[self.currentMode]['code']
        self.game = Game(board, mode)
        self.cellSize = min(
            math.floor(self.boardWidth / self.game.boardSize[0]), 
            math.floor(self.boardHeight / self.game.boardSize[1])
        )
        self.marginX = (self.windowWidth - self.cellSize * self.game.boardSize[0]) / 2
        self.marginY = 20

    def startGame(self):
        self.initGame()
        self.player1 = Human("Player Blue", self)
        #self.aiPlayer = AiPlayer("Ai Player", self.game)
        #self.aiPlayer = Random("Ai Player", self.game)
        #self.aiPlayer = AiMonteCarlo("Ai Player", self.game)
        #self.aiPlayer.setWait(1)
        #self.player2 = self.aiPlayer
        self.player2 = Human("Player Red", self)
        self.game.reset()
        self.game.addPlayer(self.player1)
        self.game.addPlayer(self.player2)
        self.gameState = self.STATE_GAME
        self.game.timeLimit = self.TIMES[self.timeOption]
        self.game.start()

    def stopGame(self):
        self.currentMenu = self.MENU_MAIN
        self.gameState = self.STATE_MENU
        self.game.isRunning = False

    def exit(self):
        pygame.quit()
        sys.exit()

    def displayBackgroud(self):
        self.screen.fill("lightgrey")
        if self.gameState != self.STATE_GAME:
            now = pygame.time.get_ticks()

            if not hasattr(self, 'menuCellWithColor') or now - self.menuCellColorChangeTime > 1000:
                self.menuCellWithColor = (random.randrange(self.game.boardSize[0]), random.randrange(self.game.boardSize[1]))
                self.menuCellColorChangeTime = now

            posX, posY = pygame.mouse.get_pos()
            cell = self.getCellByPosition(posX, posY, False)
            for x in range(0, self.game.boardSize[0]):
                for y in range(0, self.game.boardSize[1]):
                    hasColor = False
                    if (cell != False and x == cell[0] and y == cell[1]):
                       isMouseOver = True
                    else:
                        isMouseOver = False

                    if isMouseOver:
                        hasColor = True

                    if x == self.menuCellWithColor[0] and y == self.menuCellWithColor[1]:
                        hasColor = True

                    if ((x + y) % 2 == 0):
                        color = (205,205,205)
                        if hasColor:
                            color = color = (190,190,230)
                        self.printO(x , y, color)
                    else:
                        color = (205,205,205)
                        if hasColor:
                            color = color = (230,190,190)
                        self.printX(x , y, color)

    def trainAi(self):
        print("start training")
        self.aiPlayer.setWait(0)
        self.aiTrainer = AiTrainer(self.aiPlayer)
        self.gameState = self.STATE_TAINING

    def stopTrainAi(self):
        self.gameState = self.STATE_MENU

    def run(self):
        while True:
            self.events.reset();
            if self.events.QUIT:
                self.exit()
            self.displayBackgroud()
            if self.gameState == self.STATE_TAINING:
                self.aiTrainer.run(self.game, 10)
                if (self.aiTrainer.isFinished()):
                    self.gameState = self.STATE_MENU
            if self.gameState == self.STATE_GAME:
                self.game.run(self.events)
                self.printGame()
            else:
                self.printMenu()
            pygame.display.flip()

ticTacToe = TicTacToe()
ticTacToe.run()