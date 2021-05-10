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
from math import sqrt

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
        # Collect legal moves and child states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best
        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        The evaluation function takes in the current and proposed child
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        childGameState = currentGameState.getPacmanNextState(action)
        newPos = childGameState.getPacmanPosition()
        newFood = childGameState.getFood()
        newGhostStates = childGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
        return childGameState.getScore()

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
    Your minimax agent
    """

    def getAction(self, gameState):
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.

        Here are some method calls that might be useful when implementing minimax.

        gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

        gameState.getNextState(agentIndex, action):
        Returns the child game state after an agent takes an action

        gameState.getNumAgents():
        Returns the total number of agents in the game

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        # Begin your code (Part 1)
        act, val = self.value(gameState, 0, 0)
        return act
        
    

    def value(self, gameState, player, current_depth):
        '''
        return (action, value)
        '''
        if current_depth >= self.depth and player == 0:
            return 0, self.evaluationFunction(gameState)
        if gameState.isWin() or gameState.isLose():
            return 0, self.evaluationFunction(gameState)

        if player == 0:
            current_depth += 1
            return self.max_value(gameState, player, current_depth)
        else:
            return self.min_value(gameState, player, current_depth)

        return 0

    def max_value(self, gameState, player, current_depth):
        '''
        return (action, value)
        '''
        v = -99999999
        ret_act = None
        action_list = gameState.getLegalActions(player)
        for action in action_list:
            next_state = gameState.getNextState(player, action)
            next_player = (player + 1) % gameState.getNumAgents()
            act, val = self.value(next_state, next_player, current_depth)
            if val > v:
                v = val
                ret_act = action

        return ret_act, v

    def min_value(self, gameState, player, current_depth):
        '''
        return (action, value)
        '''
        v = 99999999
        ret_act = None
        action_list = gameState.getLegalActions(player)
        for action in action_list:
            next_state = gameState.getNextState(player, action)
            next_player = (player + 1) % gameState.getNumAgents()
            act, val = self.value(next_state, next_player, current_depth)
            if val < v:
                v = val
                ret_act = action

        return ret_act, v

        # End your code (Part 1)
    


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning
    """

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        # Begin your code (Part 2)
        act, val = self.value(gameState, 0, 0, -99999999, 99999999)
        return act
        
    
    def value(self, gameState, player, current_depth, alpha, beta):
        '''
        return (action, value)
        '''
        if current_depth >= self.depth and player == 0:
            return 0, self.evaluationFunction(gameState)
        if gameState.isWin() or gameState.isLose():
            return 0, self.evaluationFunction(gameState)

        if player == 0:
            current_depth += 1
            return self.max_value(gameState, player, current_depth, alpha, beta)
        else:
            return self.min_value(gameState, player, current_depth, alpha, beta)

        return 0

    def max_value(self, gameState, player, current_depth, alpha, beta):
        '''
        return (action, value)
        '''
        v = -99999999
        ret_act = None
        action_list = gameState.getLegalActions(player)
        for action in action_list:
            next_state = gameState.getNextState(player, action)
            next_player = (player + 1) % gameState.getNumAgents()
            act, val = self.value(next_state, next_player, current_depth, alpha, beta)
            if val > v:
                v = val
                ret_act = action
            if v > beta:
                return ret_act, v
            alpha = max(alpha, v)

        return ret_act, v

    def min_value(self, gameState, player, current_depth, alpha, beta):
        '''
        return (action, value)
        '''
        v = 99999999
        ret_act = None
        action_list = gameState.getLegalActions(player)
        for action in action_list:
            next_state = gameState.getNextState(player, action)
            next_player = (player + 1) % gameState.getNumAgents()
            act, val = self.value(next_state, next_player, current_depth, alpha, beta)
            if val < v:
                v = val
                ret_act = action
            if v < alpha:
                return ret_act, v
            beta = min(beta, v)

        return ret_act, v

        # End your code (Part 2)

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent
    """

    def getAction(self, gameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        # Begin your code (Part 3)
        act, val = self.value(gameState, 0, 0)
        return act
        
    def value(self, gameState, player, current_depth):
        '''
        return (action, value)
        '''
        if current_depth >= self.depth and player == 0:
            return 0, self.evaluationFunction(gameState)
        if gameState.isWin() or gameState.isLose():
            return 0, self.evaluationFunction(gameState)

        if player == 0:
            current_depth += 1
            return self.max_value(gameState, player, current_depth)
        else:
            return self.expect_value(gameState, player, current_depth)

        return 0

    def max_value(self, gameState, player, current_depth):
        '''
        return (action, value)
        '''
        v = -99999999
        ret_act = None
        action_list = gameState.getLegalActions(player)
        for action in action_list:
            next_state = gameState.getNextState(player, action)
            next_player = (player + 1) % gameState.getNumAgents()
            act, val = self.value(next_state, next_player, current_depth)
            if val > v:
                v = val
                ret_act = action

        return ret_act, v

    def expect_value(self, gameState, player, current_depth):
        '''
        return (action, value)
        '''
        ret_act = None
        action_list = gameState.getLegalActions(player)
        total = 0
        for action in action_list:
            next_state = gameState.getNextState(player, action)
            next_player = (player + 1) % gameState.getNumAgents()
            act, val = self.value(next_state, next_player, current_depth)
            total += val

        return ret_act, total / len(action_list)

        # End your code (Part 3)
    




def betterEvaluationFunction(currentGameState):
    """
    Your extreme evaluation function
    """
    # Begin your code (Part 4)
    pacman = currentGameState.getPacmanPosition()

    ret = 2*currentGameState.getScore()
    if currentGameState.isLose():
        ret += -9999999
    if currentGameState.isWin():
        ret += 9999999

    for capsule_loc in currentGameState.getCapsules():
        ret -= 10 * distance(pacman, capsule_loc)
    ret += 1000 - 200 * len(currentGameState.getCapsules())

    for ghost in currentGameState.getGhostStates():
        if ghost.scaredTimer > 5:
            ret -= 20*distance(pacman, ghost.getPosition())
        else:
            ret += 5*distance(pacman, ghost.getPosition())
    
    ret += 1000 - 20*currentGameState.getNumFood()
    
    currentFood = currentGameState.getFood()
    for i, d in enumerate(currentGameState.getFood()):
        for j, e in enumerate(d):
            if currentFood[i][j] == True:
                ret -= distance(pacman, (i,j))
    return ret

def distance(l1, l2):
    return sqrt((l1[0] - l2[0]) ** 2 + (l1[1] - l2[1]) ** 2)
    
    # End your code (Part 4)

# Abbreviation
better = betterEvaluationFunction
