from queues import PriorityQueue

MAX_GRID_X = 4
MAX_GRID_Y = 4

def available_states(state):
  position = state[0]
  actions = []

  if (position[1] < MAX_GRID_Y):
    actions.append('UP')
  if (position[1] > 1):
    actions.append('DOWN')
  if (position[0] > 1):
    actions.append('LEFT')
  if (position[0] < MAX_GRID_X):
    actions.append('RIGHT')

  return [transaction(state, action) for action in actions]

def transaction(state, action):
  (position, pellets) = state

  if action == 'UP' and position[1] < MAX_GRID_Y:
    position = (position[0], position[1]+1)
  elif action == 'DOWN' and position[1] > 1:
    position = (position[0], position[1]-1)
  elif action == 'LEFT' and position[0] > 1:
    position = (position[0]-1, position[1])
  elif action == 'RIGHT' and position[0] < MAX_GRID_X:
    position = (position[0]+1, position[1])

  new_pellets = []

  for pellet in pellets:
    if not pellet == position:
      new_pellets.append(pellet)

  return (position, new_pellets)

def is_goal(state):
  return len(state[1]) == 0

def heuristic(state):
  (position, pellets) = state

  sum = 0
  for pellet in pellets:
    sum += abs(pellet[0] - position[0]) + abs(pellet[1] - position[1])

  return sum

def bfs(state):
  frontier = [state]
  explored = []
  first_ate = None

  while len(frontier) > 0:
    current = frontier.pop(0)
    
    if (len(start_state[1]) > len(current[1])) and first_ate is None:
      first_ate = list(set(start_state[1]) - set(current[1]))[0]
      print(f"First ate = {first_ate}")

    explored.append(current[0])

    if (is_goal(current)):
      print(f"Last ate = {current[0]}")
      return explored
    
    next_fronter = []

    for next_state in available_states(current):
      if next_state[0] not in explored:
        next_fronter.append(next_state)

    frontier = next_fronter + frontier

def greedy_search(start_state):
  frontier = PriorityQueue()
  frontier.push(start_state, heuristic(start_state))

  explored = []
  first_ate = None

  while frontier.len() > 0:
    current = frontier.pop()

    if (len(start_state[1]) > len(current[1])) and first_ate is None:
      first_ate = list(set(start_state[1]) - set(current[1]))[0]
      print(f"First ate = {first_ate}")

    explored.append(current[0])

    if (is_goal(current)):
      print(f"Last ate = {current[0]}")
      return explored

    choices = available_states(current)
    for choice in choices:
      frontier.push(choice, heuristic(choice))

if __name__ == "__main__":
  start_state = ((4,3), [(4,4), (1,4), (2,3), (2,2), (3,1)])

  print("BFS:")
  bfs(start_state)

  print("GREEDY:")
  greedy_search(start_state)
