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
        # Collect legal moves and child states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

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

        "*** YOUR CODE HERE ***"
        (newPosX, newPosY) = newPos

        nearest_food_dist = None # Minimize this
        manhatten_sum = 0

        for x in range(0,newFood.width):
            for y in range(0, newFood.height):
                if newFood[x][y]:
                    manh_dist = abs(x - newPosX) + abs(y - newPosY)
                    manhatten_sum += manh_dist
                    if nearest_food_dist is None or nearest_food_dist > manh_dist:
                        nearest_food_dist = manh_dist

        stop_tax = 0
        if action == 'Stop':
            stop_tax = -100

        same_direction_bonus = 0
        if action == currentGameState.getPacmanState().getDirection():
            same_direction_bonus = 10

        if manhatten_sum == 0: # game won
            return childGameState.getScore() + 100

        return ((100+same_direction_bonus)/manhatten_sum) + childGameState.getScore() + stop_tax

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
        "*** YOUR CODE HERE ***"
        def get_action_score_tuple_score(e):
            return e[1]

        tree_height = 1 + (self.depth * gameState.getNumAgents())

        def recursive_minimax(cur_game_state, agents_turn, tree_depth):
            '''
            returns are tuple (action to take at given state, score you will receive)
            '''
            if cur_game_state.isWin() or cur_game_state.isLose() or tree_depth == (tree_height-1):
                return (None, cur_game_state.getScore())

            is_max = agents_turn == 0
            next_agent = (agents_turn + 1) % cur_game_state.getNumAgents()
            legal_actions = cur_game_state.getLegalActions(agents_turn)

            # recursive case:
            next_states = [] # (action to take, score you'll get)
            for action in legal_actions:
                next_state = cur_game_state.getNextState(agents_turn, action)
                (_, action_score) = recursive_minimax(next_state, next_agent, tree_depth+1)
                next_states.append((action, action_score))

            if is_max:
                return max(next_states, key=get_action_score_tuple_score)
            
            return min(next_states, key=get_action_score_tuple_score)

        return recursive_minimax(gameState, 0, 0)[0]

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        tree_height = 1 + (self.depth * gameState.getNumAgents())

        def recursive_alpha_beta(cur_game_state, agents_turn, tree_depth, alpha, beta):
            '''
            returns (action to take at cur_game_state to get value, value)
            '''
            if cur_game_state.isWin() or cur_game_state.isLose() or tree_depth == (tree_height-1):
                return (None, cur_game_state.getScore())
            
            is_max = agents_turn == 0
            next_agent = (agents_turn + 1) % cur_game_state.getNumAgents()
            best_value = float('inf')
            best_action = None

            if is_max:
                best_value = best_value * -1

            for action in cur_game_state.getLegalActions(agents_turn):
                next_state = cur_game_state.getNextState(agents_turn, action)
                (_, next_value) = recursive_alpha_beta(next_state, next_agent, tree_depth+1, alpha, beta)

                if is_max: # MAX_VALUE
                    if next_value > best_value:
                        best_value = next_value
                        best_action = action
                        alpha = max([best_value, alpha])
                    if best_value > beta:
                        return (best_action, best_value) # prune
                else: # MIN_VALUE
                    if next_value < best_value:
                        best_value = next_value
                        best_action = action
                        beta = min([beta, best_value])
                    if best_value < alpha:
                        return (best_action, best_value) # prune

            return (best_action, best_value)

        return recursive_alpha_beta(gameState, 0, 0, -float('inf'), float('inf'))[0]

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
        def get_action_score_tuple_score(e):
            return e[1]

        tree_height = 1 + (self.depth * gameState.getNumAgents())

        def recursive_expectimax(cur_game_state, agents_turn, tree_depth):
            '''
            returns are tuple (action to take at given state, score you will receive)
            '''
            if cur_game_state.isWin() or cur_game_state.isLose() or tree_depth == (tree_height-1):
                return (None, cur_game_state.getScore())

            is_pacman = agents_turn == 0
            next_agent = (agents_turn + 1) % cur_game_state.getNumAgents()
            legal_actions = cur_game_state.getLegalActions(agents_turn)

            # recursive case:
            next_states = [] # (action to take, score you'll get)
            for action in legal_actions:
                next_state = cur_game_state.getNextState(agents_turn, action)
                (_, action_score) = recursive_expectimax(next_state, next_agent, tree_depth+1)
                next_states.append((action, action_score))

            if is_pacman:
                return max(next_states, key=get_action_score_tuple_score)
            
            #compute expected value:
            return (None, sum([v for (_, v) in next_states])/len(next_states))

        return recursive_expectimax(gameState, 0, 0)[0]

def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()    

# Abbreviation
better = betterEvaluationFunction
