__author__ = 'rsimpson'


"""
I started with minimax code that I found here:
http://callmesaint.com/python-minimax-tutorial/
That code was written by Matthew Griffin

Then I added in code I got from here:
https://inventwithpython.com/tictactoe.py
That code was written by Al Sweigart

Then I started adding my own code
"""

from gobbletConstants import *
from gobbletMachine import *
import copy

DEPTHLIMIT = 3 # change depth of AlphaBeta to 3

class AlphaBetaMachine(Machine):
    def __init__(self, _name):
        # call constructor for parent class
        Machine.__init__(self, _name)
        # corner indexes for board
        self.corners = [0, 3, 12, 15]
        # center indexes for board
        self.centers = [5, 6, 9, 10]
        # pair indexes for board
        self.pairs = [
            [(0,1),(0,4),(0,5)],# 0
            [(1,2),(1,4),(1,5),(1,6)],# 1
            [(2,3),(2,5),(2,6),(2,7)],# 2
            [(3,6),(3,7)],# 3
            [(4,5),(4,8),(4,9)],# 4
            [(5,6),(5,8),(5,9),(5,10)],# 5
            [(6,7),(6,9),(6,10),(6,11)],# 6
            [(7,10),(7,11)],# 7
            [(8,9),(8,12),(8,13)],# 8
            [(9,10),(9,12),(9,13),(9,14)],# 9
            [(10,11),(10,13),(10,14),(10,15)],# 10
            [(11,14),(11,15)],# 11
            [(12,13)],# 12
            [(13,14)],# 13
            [(14,15)]# 14
            # 15 empty
        ]
        # caddy corner indexes for board
        self.caddy_corners = [

        ]
        # pair/caddy score multiplier
        self.SCORE_PAIR = 5
        # corner score multiplier
        self.SCORE_CORNER = 10
        # center score multiplier
        self.SCORE_CENTER = 20

    def getPieces(self, player):
        """Returns players pieces list from constants.
        :param player: string of player name.
        :return: players pieces list.
        """
        if player == 'O':
            return O_PIECES
        elif player == 'X':
            return X_PIECES
        else:
            print "Error AB Line 59"
            return []

    def calculateCorners(self, board, pieces):
        """Sends back int of how many corners are controller by player.
        :param board: current board list.
        :param pieces: player being checked pieces array.
        :return: int of how many corners are controller by player.
        """
        num = 0 # number of corners

        for corner in self.corners: # for each corner piece check if someone controls it
            if len(board[corner]) > 0: # prevent index out of range
                if board[corner][-1] in  pieces: # check if the top piece is player's piece
                    num += 1 # corner controlled

        return num

    def calculateCenters(self, board, pieces):
        """Sends back int of how many centers are controller by player.
        :param board: current board list.
        :param pieces: player being checked pieces array.
        :return: int of how many centers are controller by player.
        """
        num = 0 # number of centers

        for center in self.centers: # for each center piece check if someone controls it
            if len(board[center]) > 0: # prevent index out of range
                if board[center][-1] in  pieces: # check if the top piece is player's piece
                    num += 1 # center controlled

        return num

    def calculatePairs(self, board, pieces):
        """Sends back int of how many pairs are controller by player.
        :param board: current board list.
        :param pieces: player being checked pieces array.
        :return: int of how many pairs are controller by player.
        """
        num = 0 # number of pairs

        for square in self.pairs: # for each square piece get list of pairs
            for pair in square: # for each pair check if someone controls it
                if len(board[pair[0]]) > 0 and len(board[pair[1]]) > 0: # prevent index out of range
                    # check if the top piece is player's piece in both pair values
                    if board[pair[0]][-1] in  pieces and board[pair[1]][-1] in  pieces:
                        num += 1 # pair controlled

        return num

    def evaluationFunction(self, _board):
        """
        This function is used by minimax to evaluate a non-terminal state.
        """
        # start with a value of zero
        score = 0
        board = _board.board
        # add number of pairs we have
        score += self.SCORE_PAIR * self.calculatePairs(board, self.getPieces(self.name))
        # subtract number of pairs opponent has
        score -= self.SCORE_PAIR * self.calculatePairs(board, self.getPieces(self.opponent))
        # add number of corners we have
        score += self.SCORE_CORNER * self.calculateCorners(board, self.getPieces(self.name))
        # subtract number of corners opponent has
        score -= self.SCORE_CORNER * self.calculateCorners(board, self.getPieces(self.opponent))
        # add number of centers we have
        score += self.SCORE_CENTER * self.calculateCenters(board, self.getPieces(self.name))
        # subtract number of centers opponent has
        score -= self.SCORE_CENTER * self.calculateCenters(board, self.getPieces(self.opponent))
        # return the evaluation score

        return score

    def atTerminalState(self, _board, _depth):
        """
        Checks to see if we've reached a terminal state. Terminal states are:
           * somebody won
           * we have a draw
           * we've hit the depth limit on our search
        Returns a tuple (<terminal>, <value>) where:
           * <terminal> is True if we're at a terminal state, False if we're not
           * <value> is the value of the terminal state
        """
        global DEPTHLIMIT
        # Yay, we won!
        if _board.isWinner(self.myPieces):
            # Return a positive number
            return (True, BIG_POSITIVE_NUMBER)
        # Darn, we lost!
        elif _board.isWinner(_board.opponentPieces(self.name)):
            # Return a negative number
            return (True, BIG_NEGATIVE_NUMBER)
        # if we've hit our depth limit
        elif (_depth >= DEPTHLIMIT):
            # use the evaluation function to return a value for this state
            return (True, self.evaluationFunction(_board))
        return (False, 0)

    def alphaBetaMax(self, _board, _depth = 0, _alpha = NEGATIVE_INFINITY, _beta = POSITIVE_INFINITY):
        '''
        This is the MAX half of alpha-beta pruning. Here is the algorithm:

        int alphaBetaMax( int alpha, int beta, int depthleft ) {
           if ( depthleft == 0 ) return evaluate();
           for ( all moves) {
              score = alphaBetaMin( alpha, beta, depthleft - 1 );
              if( score >= beta )
                 return beta;   // fail hard beta-cutoff
              if( score > alpha )
                 alpha = score; // alpha acts like max in MiniMax
           }
           return alpha;
        }
        '''
        #
        # At a terminal state
        #
        # check to see if we are at a terminal state - someone won or we hit our search limit
        terminalTuple = self.atTerminalState(_board, _depth)
        # if we are at a terminal state
        if terminalTuple[0] == True:
            # return the value of this state
            return (0, terminalTuple[1])
        #
        # Not at a terminal state, so search further...
        #
        # get all my legal moves
        possibleMoves = _board.possibleNextMoves(self.myPieces)
        # pick a random move as a default
        bestMove = random.choice(possibleMoves)
        # loop through all possible moves
        for m in possibleMoves:
            if (_depth == 0):
                pass
                #print 'considering ' + str(m),
            # keep a copy of the old board
            oldBoard = copy.deepcopy(_board.board)
            # make the move - move is a tuple: (piece, square)
            _board.makeMove(m[0], m[1])
            # get the minimax vaue of the resulting state - returns a tuple (move, score)
            (mv, score) = self.alphaBetaMin(_board, _depth+1, _alpha, _beta)
            # undo the move
            _board.board = copy.deepcopy(oldBoard)
            if (_depth == 0):
                pass
                #print ' score = ' + str(score)
            # compare score to beta - can we prune?
            if (score >= _beta):
                return (mv, _beta)
            # compare score to alpha - have we found a better move?
            if (score > _alpha):
                # keep the better move
                bestMove = m
                # update alpha
                _alpha = score
        # return the best move we found
        return (bestMove, _alpha)

    def alphaBetaMin(self, _board, _depth, _alpha, _beta):
        '''
        This is the MIN half of alpha-beta pruning. Here is the general algorithm:

        int alphaBetaMin( int alpha, int beta, int depthleft ) {
           if ( depthleft == 0 ) return -evaluate();
           for ( all moves) {
              score = alphaBetaMax( alpha, beta, depthleft - 1 );
              if( score <= alpha )
                 return alpha; // fail hard alpha-cutoff
              if( score < beta )
                 beta = score; // beta acts like min in MiniMax
           }
           return beta;
        }
        '''
        #
        # At a terminal state
        #
        # check to see if we are at a terminal state - someone won or we hit our search limit
        terminalTuple = self.atTerminalState(_board, _depth)
        # if we are at a terminal state
        if terminalTuple[0] == True:
            # return the value of this state
            return (0, terminalTuple[1])
        #
        # Not at a terminal state, so search further...
        #
        # get all my opponent's legal moves
        possibleMoves = _board.possibleNextMoves(_board.opponentPieces(self.name))
        # pick a random move as a default
        bestMove = random.choice(possibleMoves)
        # consider all possible moves
        for m in possibleMoves:
            # keep a copy of the old board
            oldBoard = copy.deepcopy(_board.board)
            # make the move
            _board.makeMove(m[0], m[1])
            # get the minimax vaue of the resulting state - returns a tuple (move, score)
            (mv, score) = self.alphaBetaMax(_board, _depth+1, _alpha, _beta)
            # undo the move
            _board.board = copy.deepcopy(oldBoard)
            # compare score to alpha - can we prune?
            if (score <= _alpha):
                return (m, _alpha)
            # compare score to the best move we found so far
            if (score < _beta):
                _beta = score
        # send back the best move we found
        return (bestMove, _beta)

    def move(self, _board):
        m = self.alphaBetaMax(_board)[0]
        print "move = " + str(m)
        return m

