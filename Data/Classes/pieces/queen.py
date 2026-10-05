import pygame
from Data. Classes. piece import Piece

class Queen(Piece):
    def __init__ (self, position, colour, board):
        #Gives access to the parent class's attributes and methods
        super().__init__(position, colour, board)
        #Loads the image and scales it to be 10 pixels shorter and thinner than the square
        img = 'Data/imgs/' + colour[0] + 'Q.png'
        self.img = pygame.image.load(img)
        self.img = pygame.transform.scale(self.img, (board.square_width - 10, board.square_height - 10))
        #Notation of the queen is 'Q'
        self.notation = 'Q'
        
    def get_possible_moves (self, board):
        availiable_squares = []
        north = []
        east = []
        south = []
        west = []
        ne = []
        nw = []
        sw = []
        se = []
        
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