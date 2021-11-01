import random
from helper import V, Board


def avoid_board(board, possible_moves):
    new_possible_moves = {}
    for move, pos in possible_moves.items():
        if board[pos] < 15:
            new_possible_moves[move] = pos
    return new_possible_moves


def floot_fill_calc(pos, board, visited, from_danger=False):
    if from_danger and board[pos] == 0:
        return 1
    if pos in visited:
        return 0
    if board[pos] != 0:
        visited.add(pos)
        if board[pos] > 999:
            return 0
        return (floot_fill_calc(pos + V("up")   , board, visited, True) +
                floot_fill_calc(pos + V("down") , board, visited, True) +
                floot_fill_calc(pos + V("left") , board, visited, True) +
                floot_fill_calc(pos + V("right"), board, visited, True) + (1/board[pos]))
    else:
        visited.add(pos)
        return (floot_fill_calc(pos + V("up")   , board, visited) +
                floot_fill_calc(pos + V("down") , board, visited) +
                floot_fill_calc(pos + V("left") , board, visited) +
                floot_fill_calc(pos + V("right"), board, visited) + 1)


def food_score(pos, foods):
    score = 0
    for food in foods:
        if pos == food:
            score += 20
            continue
        score += 1 / max(1, pos.taxi(food))
    return score

def choose_move(data):
    head = V(data["you"]["head"])
    health = data["you"]["health"]
    snakes = data["board"]["snakes"]
    for snake in snakes:
        snake["body"] = [V(x) for x in snake["body"]]
    hazzards = [V(x) for x in data["board"]["hazards"]]

    board_width = data["board"]["height"]
    board_height = data["board"]["height"]

    board = Board(board_width, board_height)
    for snake in snakes:
        board.add_snake(snake["body"], head, (snake["id"] != data["you"]["id"] and snake["length"] >= data["you"]["length"]))
    board.add_hazzards(hazzards)

    foods = []
    best_food = None
    best_food_dist = None
    for food in data["board"]["food"]:
        foods.append(V(food))
        if best_food_dist is None or head.taxi(V(food)) < best_food_dist:
            best_food = V(food)
            best_food_dist = head.taxi(best_food)
    if foods:
        if head in hazzards:
            if health / 16 > best_food_dist:
                foods = [best_food]
            else:
                for x in range(board_width):
                    for y in range(board_height):
                        if V(x, y) not in hazzards:
                            foods.append(V(x, y))
        else:
            foods = [f for f in foods if f not in hazzards]

    possible_moves = {
        "up"   : head + V("up"),
        "down" : head + V("down"),
        "left" : head + V("left"),
        "right": head + V("right"),
        }
    possible_moves = avoid_board(board, possible_moves)

    moves = list(possible_moves.items())
    random.shuffle(moves)
    
    if foods:
        moves.sort(key=lambda x: food_score(x[1], foods), reverse=True)
    # list(map(lambda x: print(x[0], int(floot_fill_calc(x[1], board, set()))), moves))
    
    moves.sort(key=lambda x: int(floot_fill_calc(x[1], board, set())), reverse=True)
    
    if moves:
        move = moves[0][0]
    else:
        move = "up"

    #print(f"{data['game']['id']} MOVE {data['turn']}: {move} picked from all valid options in {possible_moves}")
    print("<" + "#" * max(0, data["you"]["length"] - 2) + f"B {data['you']['health']: >3} {move}                                 ", end="\r")
    return move
