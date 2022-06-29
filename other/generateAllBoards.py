import sys
sys.path.append('..')

from game import Game, MoveError

boards = set()
def generate_all_boards(game: Game, player: int = 0):
    if (game.board1, game.board2) in boards:
        return
    boards.add((game.board1, game.board2))
    for column in range(7):
        try:
            game.make_move(column, player)
            generate_all_boards(game, 1 - player)
            game.undo_move()
        except MoveError:
            pass

import time
start = time.perf_counter()

generate_all_boards(Game())

end = time.perf_counter()
print(len(boards))
print(f'time: {end - start}')

with open('boards.txt', 'w') as f:
    f.write(str(boards))
