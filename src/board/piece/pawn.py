from . import Piece, Color, Move
import numpy as np

class Pawn(Piece):

    def __init__(self, square: np.array, color: Color):
        super().__init__(square, color, 1)

        # Assume that has moved if not on the second or 7th rank
        if square is not None and square[0] != 1 and square[0] != 6:
            self.nr_moves = 1

    def calculate_controlled_squares(self, board: np.array):
        # TODO think this through because technically the pawn doesn't
        # control the squares in front of it
        self.controlled_squares = np.vstack((self.get_advances(board), self.get_captures(board)))    

    def get_advances(self, board: np.array) -> np.array:
        possible_squares = np.empty((0,2), dtype=int)
        # If white, move up the board, down otherwise
        direction = 1 if self.color == Color.White else -1

        sqr_1 = np.copy(self.square)
        sqr_1[0] += direction # Move 1 square
        move_1_possible = self.is_on_board(sqr_1) and board[tuple(sqr_1)] is None
        if not move_1_possible:
            return possible_squares # moving 2 squares cannot be possible either in this case
        possible_squares = np.vstack((possible_squares, sqr_1))

        if self.nr_moves > 0:
            return possible_squares
        
        sqr_2 = np.copy(self.square)
        sqr_2[0] += 2*direction # Move 2 squares
        if self.is_on_board(sqr_2) and board[tuple(sqr_2)] is None:
            possible_squares = np.vstack((possible_squares, sqr_2))

        return possible_squares
    
    def get_captures(self, board: np.array) -> np.array:
        possible_squares = np.empty((0,2), dtype=int)
        # If white, move up the board, down otherwise
        direction = 1 if self.color == Color.White else -1

        capture_1 = np.copy(self.square)
        capture_1 += (direction, 1)
        if self.is_on_board(capture_1):
            piece_to_capture = board[tuple(capture_1)]
            if piece_to_capture is not None and \
                piece_to_capture.color != self.color:

                possible_squares = np.vstack((possible_squares, capture_1))
                piece_to_capture.attacked_by.append(self)

        capture_2 = np.copy(self.square)
        capture_2 += (direction, -1)
        if self.is_on_board(capture_2):
            piece_to_capture = board[tuple(capture_2)]
            if piece_to_capture is not None and \
                piece_to_capture.color != self.color:

                possible_squares = np.vstack((possible_squares, capture_2))
                piece_to_capture.attacked_by.append(self)

        return possible_squares
    
    def fen_symbol(self):
        if self.color == Color.White:
            return "P"
        return "p"