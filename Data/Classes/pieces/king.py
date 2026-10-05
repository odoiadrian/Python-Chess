import pygame
from Data. Classes. piece import Piece

class King(Piece):
    def __init__ (self, position, colour, board):
        #Gives access to the parent class's attributes and methods
        super().__init__(position, colour, board)
        #Loads the image and scales it to be 10 pixels shorter and thinner than the square
        img = 'Data/imgs/' + colour[0] + 'K.png'
        self.img = pygame.image.load(img)
        self.img = pygame.transform.scale(self.img, (board.square_width - 10, board.square_height - 10))
        #Notation of the king is 'K'
        self.notation = 'K'
                            
        
    def get_possible_moves(self, board):
        availiable_squares = []
        moves = [
            (0,-1), # north
            (1, -1), # northeast
            (1, 0), # east
            (1, 1), # southeast
            (0, 1), # south
            (-1, 1), # southwest
            (-1, 0), # west
            (-1, -1), # northwest
        ]
        for move in moves:
            #Gets the square of the potential move
            new_position = (self.x + move[0], self.y + move[1])
            #Checks if the square is on the board
            if (new_position[0] <= 7 and new_position[0] >= 0 and new_position[1] <= 7 and new_position[1] >= 0):
                availiable_squares.append([board.get_square_from_position(new_position)])
        
        #Gets the squares that can be castled to
        if list(self.castling(board)) != []:
            for move in self.castling(board):
                availiable_squares.append(move)
        return availiable_squares
    
    #Returns the squares if that can be castled to
    def castling(self, board):
        castles = []
        blocking_piecesK = []
        blocking_piecesQ = []
        if board.wcheck == True or board.bcheck == True:
            return []
        #Collects any pieces that may be blocking the rook and king
        for i in range(1, 4):
            blocking_piecesQ.append(board.get_piece_from_position((i, self.y)))
        for i in range(5, 7):
             blocking_piecesK.append(board.get_piece_from_position((i, self.y)))
             
        #Sets castling squares provided that nothing's in the way and neither the king and respective rook have moved
        if blocking_piecesQ == [None, None, None] and self.has_moved == False and board.get_piece_from_position((0, self.y)) and board.get_piece_from_position((0, self.y)).has_moved == False:
            castles.append(board.get_square_from_position((2, self.y)))
        if blocking_piecesK == [None, None]and self.has_moved == False and board.get_piece_from_position((7, self.y)) and board.get_piece_from_position((7, self.y)).has_moved == False:
            castles.append(board.get_square_from_position((6, self.y)))
            
        for move in castles:
            if move in self.cant_go(board):
                castles.remove(move)
            
        return castles
    
    def cant_go (self, board):
        moves = []
        for square in board.squares:
            if square.occupying_piece and square.occupying_piece.colour != self.colour and square.occupying_piece.notation == ' ' :
                for move in square.occupying_piece.attacking_squares(board):
                    moves.append(move)
        return moves