from players.random import Random
from players.aiMonteCarlo import AiMonteCarlo
import copy

class AiTrainer:
    def __init__(self, aiPlayer, gamesToPlay = 1000, generations = 50):
        self.gamesToPlay = gamesToPlay
        self.aiOpponent = AiMonteCarlo("test", aiPlayer.game)
        self.aiPlayer = aiPlayer
        self.gamesInGeneration = gamesToPlay // generations
        self.currentScore = 0
        self.bestScore = 0
        self.bestNeuralNet = copy.deepcopy(aiPlayer.neuralNet)
        self.reset()
        print("Generation size: " + str(self.gamesInGeneration))
        print("Generations: " + str(generations))

    def reset(self):
        self.currentGame = 0

    def run(self, game, moves = 1):
        currentMove = 0
        while (not self.isFinished() and currentMove < moves):
            if (not game.isRunning and self.currentGame < self.gamesToPlay):
                self.currentGame = self.currentGame + 1

                #print ("!!!" + str(game.winner))

                if (game.winner == 0):
                    self.currentScore += 0.1
                if (game.winner == 1):
                    self.currentScore += 1
                if (game.winner == -1):
                    self.currentScore -= 1

                game.reset()
                game.isRunning = True
                game.addPlayer(self.aiOpponent)
                game.addPlayer(self.aiPlayer)
                if (self.currentGame % self.gamesInGeneration == 0):
                    self.nextGeneration()
            game.run()
            #print(game.board)
            currentMove = currentMove + 1

    def isFinished(self):
        return not self.currentGame < self.gamesToPlay
    
    def nextGeneration(self):
        gen = self.currentGame // self.gamesInGeneration
        if self.currentScore > self.bestScore:
            self.bestScore = self.currentScore
            #model = clone
            self.bestNeuralNet = copy.deepcopy(self.aiPlayer.neuralNet)
            print(f"GEN {gen}: better model -> score {self.bestScore}")
        else: 
            print(f"GEN {gen}: worst model -> score {self.currentScore}")
            pass
        self.currentScore = 0
        #self.aiPlayer.neuralNet = copy.deepcopy(self.bestNeuralNet)
        if not self.isFinished():
            self.aiPlayer.neuralNet.mutate()
        else:
            self.aiPlayer.neuralNet = copy.deepcopy(self.bestNeuralNet)
