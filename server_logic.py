import random
from helper import V, Board


def avoid_board(board, possible_moves):
  new_possible_moves = {}
  for move, pos in possible_moves.items():
    if board[pos] < 15:
      new_possible_moves[move] = pos
  return new_possible_moves

def floot_fill_calc(pos, board, visited):
  if board[pos] != 0 or pos in visited:
    return 0
  else:
    visited.add(pos)
    return (floot_fill_calc(pos + V("up")   , board, visited) +
            floot_fill_calc(pos + V("down") , board, visited) +
            floot_fill_calc(pos + V("left") , board, visited) +
            floot_fill_calc(pos + V("right"), board, visited) + 1)

def choose_move(data):
    head = V(data["you"]["head"])
    body = [V(x) for x in data["you"]["body"]]
    snakes = data["board"]["snakes"]
    for snake in snakes:
      snake["body"] = [V(x) for x in snake["body"]]
    foods = [V(x) for x in data["board"]["food"]]
    #print(f"All board data this turn: {data}")

    board_width = data["board"]["height"]
    board_height = data["board"]["height"]

    board = Board(board_width, board_height)
    for snake in snakes:
      board.add_snake(snake["body"], (snake["id"] != data["you"]["id"] and snake["length"] >= data["you"]["length"]))

    possible_moves = {
      "up"   : head + V("up"),
      "down" : head + V("down"),
      "left" : head + V("left"),
      "right": head + V("right"),
      }
    possible_moves = avoid_board(board, possible_moves)

    moves = list(possible_moves.items())
    random.shuffle(moves)
    
    best_food = None
    best_food_dist = None
    for food in foods:
      dist = head.taxi(food)
      if best_food is None or dist < best_food_dist:
        best_food = food
        best_food_dist = dist

    if best_food:
      moves.sort(key=lambda x: x[1].taxi(best_food))
    
    #list(map(lambda x: print(x[0], floot_fill_calc(x[1], board, set())), moves))
    
    moves.sort(key=lambda x: floot_fill_calc(x[1], board, set()), reverse=True)
    
    if moves:
      move = moves[0][0]
    else:
      move = "up"

    #print(f"{data['game']['id']} MOVE {data['turn']}: {move} picked from all valid options in {possible_moves}")
    print("<" + "#" * max(0, data["you"]["length"] - 2) + f"B {data['you']['health']: >3} {move}                 ", end="\r")
    return move
