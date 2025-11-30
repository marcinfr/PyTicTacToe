import random
import time

class AiPlayer:
    def __init__(self, name, game):
        self.name = name
        self.game = game
        self.wait = 0
        self.startRound = False
        self.neuralNet = NeuralNet(game.boardSize * game.boardSize)

    def getMove(self, events = False):
        if (self.wait > 0):
            current_time = time.time()
            if (self.startRound == False):
                self.startRound = current_time

        if (self.wait == 0 or current_time - self.startRound > self.wait):
            board = [x for row in self.game.board for x in row]
            legalMoves = [i for i, x in enumerate(board) if x == 0]
            outputs = self.neuralNet.forward(board)

            rounded = [
                [
                    [round(v, 2) for v in row]
                    for row in matrix
                ]
                for matrix in self.neuralNet.W
            ]

            best = None
            best_val = -999

            for m in legalMoves:
                if outputs[m] > best_val:
                    best_val = outputs[m]
                    best = m
            return [best // self.game.boardSize, best % self.game.boardSize]
        return False
    
    def setWait(self, wait):
        self.wait = wait

    def endMove(self):
        self.startRound = False

class NeuralNet:
    def __init__(self, input_size, hidden_size_multiplier=3):
        self.W = []
        output_size = input_size
        hidden_size = input_size * hidden_size_multiplier
         # wagi wejście → ukryta
        self.W.append([[random.uniform(-1, 1) for _ in range(input_size)] 
                       for _ in range(hidden_size)])
        # wagi ukryta → ukryta
        self.W.append([[random.uniform(-1, 1) for _ in range(hidden_size)] 
                       for _ in range(hidden_size)])
        # wagi ukryta → wyjście
        self.W.append([[random.uniform(-1, 1) for _ in range(hidden_size)] 
                       for _ in range(output_size)])

    def processLayer(self, input, w, useRelu = True):
        output = []
        for row in w:
            s = 0
            for i in range(len(input)):
                s = s + row[i] * input[i]
            if useRelu:
                output.append(self.relu(s))
            else:
                output.append(s)
        return output
    
    def relu(self, x):
        return max(0, x)

    def forward(self, board):
        output = board
        for w in self.W:
            if w == self.W[-1]: # last layer
                relu = False
            else:
                relu = True
            output = self.processLayer(output, w, relu)
        return output
    
    def mutate(self, rate=0.1):
        """Losowa mutacja wag (do uczenia ewolucyjnego)"""
        for w in self.W:
            for i in range(len(w)):
                for j in range(len(w[i])):
                    if random.random() < rate:
                        w[i][j] += random.uniform(-0.2, 0.2)