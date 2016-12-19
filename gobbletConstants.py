# define the size of the board (NxN)
BOARD_LENGTH = 4
BOARD_SIZE = BOARD_LENGTH * BOARD_LENGTH

# define pieces owned by X and O
X_PIECES = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L']
O_PIECES = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l']

# if we reverse the pieces (so larger ones are considered before smaller ones)
# alpha-beta pruning is much more efficient
X_PIECES.reverse()
O_PIECES.reverse()

# define small, medium and large pieces - for use when comparing the size of pieces
SMALL_PIECES = ['A', 'B', 'C', 'D', 'a', 'b', 'c', 'd']
MEDIUM_PIECES = ['E', 'F', 'G', 'H', 'e', 'f', 'g', 'h']
LARGE_PIECES = ['I', 'J', 'K', 'L', 'i', 'j', 'k', 'l']

# how many turns does each player get before we declare a draw?
TURN_LIMIT = 50

# define the maximum positive number returned by the evaluation function
BIG_POSITIVE_NUMBER = 10000
BIG_NEGATIVE_NUMBER = -1 * BIG_POSITIVE_NUMBER
POSITIVE_INFINITY = BIG_POSITIVE_NUMBER * 10
NEGATIVE_INFINITY = -POSITIVE_INFINITY

# how many moves ahead does your machine player look?
# 2 means it considers its move and its opponents response
# 3 means it considers its move, its opponents response and then its countermove
# if your evaluation function is slow, your depth limit is lower; if your evaluation
# function is more efficient, you can increase the depth limit
DEPTHLIMIT = 2
