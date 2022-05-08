from Classes import SnakeClass as snake
from Classes import NeuralNetwork as nn
from Classes import NeuralNetworkVisualisation as vis

numInstances = 100 # Number of instances run each generation 
gens = 10 # The number of generations to be run
variability = 10000 # The factor by which weights and biases are changed, larger number means larger changes

boardDisplayed = 1000 # The board to be displayed to the user

def adjustNetwork(network, weightBaselines, biasBaselines, change):
    for i in range(len(network)):
        network[i].evolve(weightBaselines[i], biasBaselines[i], change)

def playGame(network, game):
    network[0].calculateActivations(snake.getNNInputs())
    for i in range(len(network)-1):
        network[i].propogate()

networks = [[nn.Input_Layer(24), nn.Hidden_Layer(18), nn.Hidden_Layer(18), nn.Hidden_Layer(4)] for i in range(numInstances)]

for i in range(numInstances):
    networkWeights = []
    networkBiases = []
    for j in range(len(networks[i])):
        networkWeights.append(networks[i][j].weights)
        networkBiases.append(networks[i][j].biases)

    adjustNetwork(networks[i], networkWeights, networkBiases, variability)

running = True
while running:
    for i in range(gens):
        games = [snake.snakeGame(16, 16, 0, 0) for i in range(numInstances)]
        bestScore = 0
        bestNetwork = 0

        for j in range(numInstances):
            if j == boardDisplayed:
                score = networks[j].learn(games[j], True)
            else:
                score = networks[j].learn(games[j], False)
            if score > bestScore:
                bestScore = score
                bestNetwork = networks[j]
        
        change = variability/bestScore
        bestSynapses = bestNetwork.synapses
        bestBiases = bestNetwork.biases
        for j in range(numInstances):
            adjustNetwork(networks[j], (bestSynapses, bestBiases), change) 
        
        print(bestScore)
    
    if input("Learn again?").lower == "n":
        running = False


    
# WORKING ON UPDATING THE Neural Network.
# Continue to debug the activations of the output layer