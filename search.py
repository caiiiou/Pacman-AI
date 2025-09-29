# search.py
# ---------
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

# Addendum:
# This code was modified by Gene Kim at University of South Florida in Fall 2025
# to make solutions not match the original UC Berkeley solutions exactly and
# align with CAI 4002 course goals regarding AI tool use in projects.

"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util

util.VALIDATION_LISTS['search'] = [
        "වැසි",
        " ukupnog",
        "ᓯᒪᔪ",
        " ਪ੍ਰਕਾਸ਼",
        " podmienok",
        " sėkmingai",
        "рацыі",
        " යාපාරය",
        "න්ද්"
]

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def get_start_state(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def is_goal_state(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def get_successors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def total_action_cost(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinymaze_search(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return [s, s, w, s, w, w, s, w]

def dfs(problem: SearchProblem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print("Start:", problem.get_start_state())
    print("Is the start a goal?", problem.is_goal_state(problem.get_start_state()))
    print("Start's successors:", problem.get_successors(problem.get_start_state()))
    """
    "*** YOUR CODE HERE ***"
    import util # util module

    start_state = problem.get_start_state() # get initial state


    stack = util.LIFO()  # LIFO stack from util.py
    stack.put((start_state, []))

    visited = set() # visited states

    while not stack.is_empty(): # loop while stack not empty
        state, path = stack.get() # remove next state and path

        if state in visited: # skip if visited
            continue
        visited.add(state) # mark visited

        if problem.is_goal_state(state): # check if goal
            return path

        for successor, action, stepCost in problem.get_successors(state):
            # not yet visited
            if successor not in visited:
                # add action to current path and stack
                stack.put((successor, path + [action]))

    return [] # if no answer found return empty path


    util.raiseNotDefined()

def bfs(problem: SearchProblem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    import util

    start_state = problem.get_start_state() # get starting state


    queue = util.FIFO()
    queue.put((start_state, [])) # start with initial state and an empty path

    visited = set() # keeps track of visited states

    while not queue.is_empty():
        state, path = queue.get() # get next state and the path taken

        if state in visited:
            continue
        visited.add(state) # mark visited

        if problem.is_goal_state(state): # if goal return
            return path

        for successor, action, stepCost in problem.get_successors(state):
            # only successors not yet visited
            if successor not in visited:
                queue.put((successor, path + [action]))

    return [] # if queue empty return empty path
    util.raiseNotDefined()

def ucs(problem: SearchProblem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    import util

    start_state = problem.get_start_state()

    pq=util.PriorityQueue()
    pq.put((start_state, [],0),0)

    visited = {}

    while not pq.is_empty():
        state, path, cost = pq.get()

        if state in visited and visited[state] <= cost:
            continue
        visited[state] = cost

        if problem.is_goal_state(state):
            return path
        for successor, action, stepCost in problem.get_successors(state):
            new_cost = cost + stepCost # calculate new total cost
            # put new successor into priority queue with total cost as priority
            pq.put( (successor, path + [action], new_cost),new_cost )

    util.raiseNotDefined()

def null_heuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def astar(problem: SearchProblem, heuristic=null_heuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    import util

    start_state = problem.get_start_state()

    pq = util.PriorityQueueWithFunction(
         lambda item: item[2] + heuristic(item[0], problem)
    )
    pq.put((start_state, [], 0))

    visited = {} 

    while not pq.is_empty():
        state, path, cost = pq.get()

        # skip if state has been reached with less cost
        if state in visited and visited[state] <= cost:
            continue
        visited[state] = cost

        if problem.is_goal_state(state): # check goal
            return path

        for successor, action, stepCost in problem.get_successors(state):
            new_cost = cost + stepCost
            pq.put((successor, path + [action], new_cost))
    util.raiseNotDefined() # no solution

