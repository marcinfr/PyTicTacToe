from helpers.resultChecker import ResultChecker
import pygame

class Game:
    MODE_CLASSIC = 'classic';
    MODE_VARNISHING = 'varnishing';

    def __init__(self, boardSize=(3, 3), linesToWin=3, mode=MODE_CLASSIC):
        self.boardSize = boardSize
        self.linesToWin = linesToWin
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
        self.lastMoves = {
            -1: [],
            1: [],
        }

    def addPlayer(self, player):
        self.players.append(player)

    def getCurrentPlayer(self):
        return self.players[int((self.currentPlayer + 2) / 2)]

    def run(self, events = False):
        if (not self.isRunning):
            return
        
        move = self.getCurrentPlayer().getMove(events);
        if (move and self.board[move[0]][move[1]] == 0):
            self.board[move[0]][move[1]] = self.currentPlayer
            self.emptyCellsQty = self.emptyCellsQty - 1

            sound = pygame.mixer.Sound("assets/click1.wav")
            sound.play()

            if self.mode == self.MODE_VARNISHING:
                self.lastMoves[self.currentPlayer].append((move[0], move[1]));
                if len(self.lastMoves[self.currentPlayer]) > self.linesToWin:
                    self.emptyCellsQty += 1
                    oldestMove = self.lastMoves[self.currentPlayer].pop(0)
                    self.board[oldestMove[0]][oldestMove[1]] = 0

            self.getCurrentPlayer().endMove()
            if (self.resultChecker.isWinningMove(self, move)):
                self.isRunning = False
                self.winner = self.currentPlayer
                return
            if (self.emptyCellsQty == 0):
                self.isRunning = 0
                return
            self.nextPlayer()

    def nextPlayer(self):
        self.currentPlayer = (-1) * self.currentPlayer
        