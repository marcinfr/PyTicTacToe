import time
import copy
import random
from helpers.resultChecker import ResultChecker
from game import Game

class AiMonteCarlo:
    def __init__(self, name, game):
        self.name = name
        self.game = game
        self.wait = 0
        self.startRound = False
        self.resultChecker = ResultChecker()

    def getMove(self, events = False):
        if (self.wait > 0):
            current_time = time.time()
            if (self.startRound == False):
                self.startRound = current_time

        if (self.wait == 0 or current_time - self.startRound > self.wait):
            return self.monte_carlo_move(self.game.board, self.game.currentPlayer)
        return False
    
    def setWait(self, wait):
        self.wait = wait

    def endMove(self):
        self.startRound = False

    def monte_carlo_move(self, board, player, simulations=200):
        moves = [(i,j) for i in range(self.game.boardSize) for j in range(self.game.boardSize) if board[i][j]==0]
        if not moves:
            return None
        scores = {move:0 for move in moves}
        for move in moves:
            for _ in range(simulations):
                b = copy.deepcopy(board)
                b[move[0]][move[1]] = player
                winner = self.random_playout(b, -player)
                if winner == player:
                    scores[move] += 1
                elif winner == 0:
                    scores[move] += 0.5  # remis
                # przegrana = 0
        best_move = max(scores, key=lambda k: scores[k])
        return best_move
    
    def random_playout(self, board, player):
        b = copy.deepcopy(board)
        g = Game(self.game.boardSize, self.game.linesToWin)
        g.currentPlayer = player
        g.board = board
        current = player
        while True:
            moves = [(i,j) for i in range(self.game.boardSize) for j in range(self.game.boardSize) if b[i][j]==0]
            move = random.choice(moves)
            b[move[0]][move[1]] = current
            if (self.resultChecker.isWinningMove(g, move, current)):
                return current
            if g.emptyCellsQty:
                return 0
            current *= -1