import pygame
from Data. Classes. piece import Piece

class Rook(Piece):
    def __init__ (self, position, colour, board):
        #Gives access to the parent class's attributes and methods
        super().__init__(position, colour, board)
        #Loads the image and scales it to be 10 pixels shorter and thinner than the square
        img = 'Data/imgs/' + colour[0] + 'R.png'
        self.img = pygame.image.load(img)
        self.img = pygame.transform.scale(self.img, (board.square_width - 10, board.square_height - 10))
        #Notation of the rook is 'R'
        self.notation = 'R'
        
    def get_possible_moves(self, board):
        availiable_squares = []
        north = []
        east = []
        south = []
        west = []
        
        #North Direction
        for y in range(self.y)[::-1]:
            north.append(board.get_square_from_position((self.x, y)))
        availiable_squares.append(north)
        
        #East Direction
        for x in range(self.x + 1, 8):
            east.append(board.get_square_from_position((x, self.y)))
        availiable_squares.append(east)
        
        #South Direction
        for y in range(self.y + 1, 8):
            south.append(board.get_square_from_position((self.x, y)))
        availiable_squares.append(south)
        
        #West Direction
        for x in range(self.x)[::-1]:
            west.append(board.get_square_from_position((x, self.y)))
        availiable_squares.append(west)
        
        return availiable_squares
