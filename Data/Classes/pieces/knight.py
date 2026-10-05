import pygame
from Data. Classes. piece import Piece

class Knight(Piece):
    def __init__ (self, position, colour, board):
        #Gives access to the parent class's attributes and methods
        super().__init__(position, colour, board)
        #Loads the image and scales it to be 10 pixels shorter and thinner than the square
        img = 'Data/imgs/' + colour[0] + 'N.png'
        self.img = pygame.image.load(img)
        self.img = pygame.transform.scale(self.img, (board.square_width - 10, board.square_height - 10))
        #Notation of the knight is 'N'
        self.notation = 'N'
        
    #Gets the squares for all knight moves (occupied squares are accounted for in the parent class)
    def get_possible_moves(self, board):
        availiable_squares = []
        moves = [
            (-2, 1),
            (-2, -1),
            (-1, 2),
            (-1, -2),
            (1, 2),
            (1, -2),
            (2, 1),
            (2, -1)
        ]
        for move in moves:
            new_position = (self.x + move[0], self.y + move[1])
            if self.x >= 0 and self.x <8 and self.y >= 0 and self.y < 8:
                availiable_squares.append(board.get_square_from_position(new_position))
        return availiable_squares