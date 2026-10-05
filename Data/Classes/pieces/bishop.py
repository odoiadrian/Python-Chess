import pygame
from Data. Classes. piece import Piece

class Bishop(Piece):
    def __init__ (self, position, colour, board):
        #Gives access to the parent class's attributes and methods
        super().__init__(position, colour, board)
        #Loads the image and scales it to be 10 pixels shorter and thinner than the square
        img = 'Data/imgs/' + colour[0] + 'B.png'
        self.img = pygame.image.load(img)
        self.img = pygame.transform.scale(self.img, (board.square_width - 10, board.square_height - 10))
        #Notation of the bishop is 'B'
        self.notation = 'B'
        
    def get_possible_moves(self, board):
        availiable_squares = []
        ne = []
        nw = []
        sw = []
        se = []
        
        #North East Direction
        for i in range(1, 8):
            if self.x + i > 7 or self.y - i < 0:
                break
            ne.append(board.get_square_from_position((self.x + i, self.y - i)))
        availiable_squares.append(ne)
        
        #North West Direction
        for i in range(1, 8):                
            if self.x - i < 0 or self.y - i < 0:
                break
            nw.append(board.get_square_from_position((self.x - i, self.y - i)))
        availiable_squares.append(nw)
        
        #South West Direction        
        for i in range(1, 8):
            if self.x - i < 0 or self.y + i > 7:
                break
            sw.append(board.get_square_from_position((self.x - i, self.y + i)))
        availiable_squares.append(sw)
        
        #South East Direction        
        for i in range(1, 8):
            if self.x + i > 7 or self.y + 1 > 7:
                break
            se.append(board.get_square_from_position((self.x + i, self.y + i)))
        availiable_squares.append(se)

        return availiable_squares