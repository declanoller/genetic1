from Board import Board
from itertools import permutations
from time import time

board_size = 8
all_boards = list(permutations(list(range(board_size)),board_size))

test_board = Board(N=board_size)
start_time = time()
for board in all_boards:
    test_board.state = list(board)
    if test_board.fitnessFunction()==0:
        print('solution found!')
        print('took this long:',time()-start_time)
        test_board.printState()
        break











#
