from helpers.resultChecker import ResultChecker
from helpers.asstes import Assets
import pygame
import math

class Game:
    MODE_CLASSIC = 'classic';
    MODE_VARNISHING = 'varnishing';

    def __init__(self, boardSettings, mode=MODE_CLASSIC):
        self.boardSettings = boardSettings
        self.boardSize = boardSettings['size']
        self.linesToWin = boardSettings['winLength']
        self.mode = mode
        self.resultChecker = ResultChecker();
        self.reset()
        self.isRunning = False

    def reset(self):
        self.board = [[0 for _ in range(self.boardSize[0])] for _ in range(self.boardSize[1])]
        self.currentPlayer = -1
        self.isRunning = False
        self.winner = 0
        self.emptyCellsQty = self.boardSize[0] * self.boardSize[1]
        self.players = []
        self.timeLimit = 0
        self.lastMoves = {
            -1: [],
            1: [],
        }

    def start(self):
        self.isRunning = True
        self.timePerMoveLeft = self.timeLimit
        self.timePerMoveInSeconds = self.timeLimit
        self.roundStartTime = pygame.time.get_ticks()

    def addPlayer(self, player):
        self.players.append(player)

    def getCurrentPlayer(self):
        return self.players[int((self.currentPlayer + 2) / 2)]

    def run(self, events = False):
        if (not self.isRunning):
            return
        
        if self.timeLimit > 0:
            self.timePerMoveLeft = self.timeLimit - (pygame.time.get_ticks() - self.roundStartTime) / 1000
            timePerMoveInSeconds = math.ceil(self.timePerMoveLeft)
            if self.timePerMoveInSeconds != timePerMoveInSeconds:
                self.timePerMoveInSeconds = timePerMoveInSeconds
                if timePerMoveInSeconds <= 0:
                    Assets.play('endtime1.wav')
                elif timePerMoveInSeconds <= 3:
                    Assets.play('tick1.wav', 0.2)
            if self.timePerMoveLeft <= 0:
                self.isRunning = False
        
        move = self.getCurrentPlayer().getMove(events);
        if (move and self.board[move[0]][move[1]] == 0):
            self.board[move[0]][move[1]] = self.currentPlayer
            self.emptyCellsQty = self.emptyCellsQty - 1

            if self.currentPlayer < 0:
                Assets.play('click1.wav')
            else:
                Assets.play('click2.wav')

            if self.mode == self.MODE_VARNISHING:
                moveToVarnishing = self.getMoveToVarnishing()
                if moveToVarnishing:
                    self.board[moveToVarnishing[0]][moveToVarnishing[1]] = 0
                    self.emptyCellsQty += 1
                    self.lastMoves[self.currentPlayer].pop(0)
                self.lastMoves[self.currentPlayer].append((move[0], move[1]));
                

            self.getCurrentPlayer().endMove()
            if (self.resultChecker.isWinningMove(self, move)):
                self.isRunning = False
                self.winner = self.currentPlayer
                Assets.play('win1.wav')
                #return
            if (self.isRunning and self.emptyCellsQty == 0):
                self.isRunning = 0
                Assets.play('draw1.wav')
                #return
            self.nextPlayer()

    def nextPlayer(self):
        self.currentPlayer = (-1) * self.currentPlayer
        self.roundStartTime = pygame.time.get_ticks()
        
    def getMoveToVarnishing(self):
        if self.mode == self.MODE_VARNISHING and self.isRunning:
            if len(self.lastMoves[self.currentPlayer]) >= self.boardSettings['varnishingElementsLimit']:
                return self.lastMoves[self.currentPlayer][0]
        return False