# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        # print(scores)
        bestScore = max(scores)
        # print(bestScore)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        # print(bestIndices)
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        # print(successorGameState)
        newPos = successorGameState.getPacmanPosition()
        # print(newPos)
        newFood = successorGameState.getFood()
        # print(newFood.asList())
        newGhostStates = successorGameState.getGhostStates()
        # newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
        
        "*** YOUR CODE HERE ***"
        currentPos = currentGameState.getPacmanPosition()
        currentFood = currentGameState.getFood()
                
        win = 9999999
        lose = -9999999
        
        for gd in newGhostStates:
            if manhattanDistance(gd.configuration.getPosition(),newPos) <= 1:
                return lose
        
        if successorGameState.isWin():
            return win
        
        foodDistance = [manhattanDistance(food,newPos) for food in newFood.asList()]
        
        foodDistancecurent = [manhattanDistance(food,currentPos) for food in currentFood.asList()]
        
        if min(foodDistance) < min(foodDistancecurent):
            return 1/(min(foodDistancecurent)-min(foodDistance)) + successorGameState.getScore()
            
        return successorGameState.getScore()

def scoreEvaluationFunction(currentGameState):
    """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
    Your minimax agent (question 2)
    """

    def getAction(self, gameState):
        # print(gameState.getLegalActions(0))
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.

        Here are some method calls that might be useful when implementing minimax.

        gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

        gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

        gameState.getNumAgents():
        Returns the total number of agents in the game

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"
        
        import math
        
        def MaxValue(gameState, d):
            d1 = d + 1
            if gameState.isWin() or gameState.isLose() or d1==self.depth:
                return self.evaluationFunction(gameState)
            vmax = -math.inf
            for a in gameState.getLegalActions(0):
                succ = gameState.generateSuccessor(0,a)
                vmax = max (vmax,MinValue(succ,d1,1))
            return vmax
        
        def MinValue(gameState, d, gno):
            vmin = math.inf
            if gameState.isWin() or gameState.isLose():   
                return self.evaluationFunction(gameState)
            for a in gameState.getLegalActions(gno):
                succ = gameState.generateSuccessor(gno,a)
                if gno == (gameState.getNumAgents() - 1):
                    vmin = min (vmin,MaxValue(succ,d))
                else:
                    vmin = min(vmin,MinValue(succ,d,gno+1))
            return vmin
        
        # import os

        value = -math.inf
        for a in gameState.getLegalActions(0):
            # os.system("pause")
            # print(gameState.generateSuccessor(0,a))
            # os.system("pause")
            valuemin = MinValue(gameState.generateSuccessor(0,a),0,1)
            if valuemin > value:
                a1 = a
                value = valuemin
        # print(a1)
        return a1
    
class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        import math
        
        def MaxValue(gameState, d, alpha, beta):
            d1 = d + 1
            newalpha = alpha
            if gameState.isWin() or gameState.isLose() or d1==self.depth:
                return self.evaluationFunction(gameState)
            vmax = -math.inf
            for a in gameState.getLegalActions(0):
                succ = gameState.generateSuccessor(0,a)
                vmax = max (vmax,MinValue(succ,d1,1,newalpha,beta))
                if vmax > beta:
                    return vmax
                newalpha = max(vmax,alpha)
            return vmax
        
        def MinValue(gameState, d, gno, alpha, beta):
            vmin = math.inf
            newbeta = beta
            if gameState.isWin() or gameState.isLose():   
                return self.evaluationFunction(gameState)
            for a in gameState.getLegalActions(gno):
                succ = gameState.generateSuccessor(gno,a)
                if gno == (gameState.getNumAgents() - 1):
                    vmin = min (vmin,MaxValue(succ,d,alpha,newbeta))
                    if vmin < alpha:
                        return vmin
                    newbeta= min(vmin, newbeta)
                else:
                    vmin = min(vmin,MinValue(succ,d,gno+1,alpha,newbeta))
                    if vmin < alpha:
                        return vmin
                    newbeta = min(newbeta, vmin)
            return vmin
        
        # import os

        value = -math.inf
        alpha = -math.inf
        beta = math.inf
        for a in gameState.getLegalActions(0):
            # os.system("pause")
            # print(gameState.generateSuccessor(0,a))
            # os.system("pause")
            valuemin = MinValue(gameState.generateSuccessor(0,a),0,1,alpha,beta)
            if valuemin > value:
                a1 = a
                value = valuemin
            if valuemin > beta:
                return a1
            alpha = max(alpha, value)
        # print(a1)
        return a1
        # util.raiseNotDefined()

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** YOUR CODE HERE ***"
        
        import math
        
        def MaxValue(gameState, d):
            d1 = d + 1
            if gameState.getLegalActions(0)==[] or d1 == self.depth:
                return self.evaluationFunction(gameState)

            vmax = -math.inf
            for a in gameState.getLegalActions(0):
                succ = gameState.generateSuccessor(0,a)
                vmax = max (vmax,ExpectValue(succ,d1,1))
            return vmax

        def ExpectValue(gameState, d, gno):
            if gameState.getLegalActions(gno)==[]:
                return self.evaluationFunction(gameState)

            
            vexp = 0
            for a in gameState.getLegalActions(gno):
                if gno == gameState.getNumAgents() - 1:
                    vexp += MaxValue(gameState.generateSuccessor(gno, a), d) / len(gameState.getLegalActions(gno))
                else:
                    vexp += ExpectValue(gameState.generateSuccessor(gno, a), d, gno+1) / len(gameState.getLegalActions(gno))
            return vexp
        
        value = -math.inf
        for a in gameState.getLegalActions(0):
            # os.system("pause")
            # print(gameState.generateSuccessor(0,a))
            # os.system("pause")
            valuemin = ExpectValue(gameState.generateSuccessor(0,a),0,1)
            if valuemin > value:
                a1 = a
                value = valuemin
        # print(a1)
        return a1

def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <I selected 4 factors which I think are important for evaluation. Most important being distance to the food.
    Other factors were distance to ghosts, number of ghosts, and food remaining. Reciprocals of quantities which we want to
    minimize are added and reciprocals of quantities to be maximized are subtracted. Weight for these terms are decided on their
    priority.>
    """

    # Useful information you can extract from a GameState (pacman.py)
    # successorGameState = currentGameState.generatePacmanSuccessor(action)
    successorGameState = currentGameState
    # print(successorGameState)
    newPos = successorGameState.getPacmanPosition()
    # print(newPos)
    newFood = successorGameState.getFood()
    # print(newFood.asList())
    newGhostStates = successorGameState.getGhostStates()
    # newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
    
    "*** YOUR CODE HERE ***"
               
    win = 9999999
    # lose = -9999999
        
    if successorGameState.isWin():
        return win
    
    foodDistance = [manhattanDistance(food,newPos) for food in newFood.asList()]
    
    ghostDistance =  [manhattanDistance(gd.configuration.getPosition(),newPos) for gd in newGhostStates]
                
    
    s1 = min(foodDistance)
    if ghostDistance != []: s2 = min(ghostDistance)
    s3 = len(foodDistance)
    if len(ghostDistance) != 0: s4 = len(ghostDistance)
    
    if s2 == 0: s2=9999999

    
    # print(s1,s2,s3,s4)
    # print (successorGameState.getScore() + 10/s1 - 10e-3/s2 + 1/s3 - 10e-3/s4)
    return successorGameState.getScore() + 1/s1 - 10e-3/s2 + 1/s3 - 10e-3/s4
# Abbreviation 
better = betterEvaluationFunction
