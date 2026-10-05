import pygame
from Data. Classes. piece import Piece

class Pawn(Piece):
    def __init__ (self, position, colour, board):
        #Gives access to the parent class's attributes and methods
        super().__init__(position, colour, board)
        #Loads the image and scales it to be 10 pixels shorter and thinner than the square
        img = 'Data/imgs/' + colour[0] + 'P.png'
        self.img = pygame.image.load(img)
        self.img = pygame.transform.scale(self.img, (board.square_width - 10, board.square_height - 10))
        #Notation of the pawn is ' '
        self.notation = ' '
        self.boosted = False
        self.en_passant = False
    
    def is_victim_valid(self, victim):
        return victim and victim.notation == ' ' and victim.boosted and not victim.stale
    
    def get_moves (self, board):
        moves = []
        available_squares = []
        
        #Gets the direction and magnitude of the move, including pawn boost
        if self.colour == 'white':
            if board.get_square_from_position((self.x, self.y-1)).occupying_piece == None:
                moves.append((0, -1))
            if not self.has_moved:
                if board.get_square_from_position((self.x, self.y-1)).occupying_piece == None:
                    moves.append((0, -2))
        elif self.colour == 'black':
            if board.get_square_from_position((self.x, self.y+1)).occupying_piece == None:
                moves.append((0, 1))
            if not self.has_moved:
                if board.get_square_from_position((self.x, self.y+1)).occupying_piece == None:
                    moves.append((0, 2))
                
        #Gets and returns the available squares based on the moves
        for move in moves:
            new_position = (self.x, self.y + move[1])
            if new_position[1] <= 7 and new_position[1] >= 0:
                available_squares.append(board.get_square_from_position(new_position))
        return available_squares
        
    def get_possible_moves (self, board):
        available_squares = []
        #Gets the squares for the normal forward movement
        for square in self.get_moves(board):
            if square.occupying_piece == None:
                available_squares.append(square)
                        
        #Get squares for En Passant
        if self.colour == 'white' and board.turn == 'white':
            if self.x + 1 <= 7 and self.y == 3:
                square = board.get_square_from_position((self.x+1, self.y-1))
                ep_square = board.get_square_from_position((self.x+1, self.y))
                victim = ep_square.occupying_piece
                if victim and victim.boosted and not victim.stale:
                    victim = ep_square.occupying_piece
                if self.is_victim_valid(victim):
                    available_squares.append(square)
                    self.en_passant = True
            
            if self.x - 1 >= 0 and self.y == 3:
                square = board.get_square_from_position((self.x-1, self.y-1))
                ep_square = board.get_square_from_position((self.x-1, self.y))
                victim = ep_square.occupying_piece
                if self.is_victim_valid(victim):
                    available_squares.append(square)
                    self.en_passant = True
                        
        elif self.colour == 'black' and board.turn == 'black':
            if self.x + 1 <= 7 and self.y == 4:
                square = board.get_square_from_position((self.x+1, self.y+1))
                ep_square = board.get_square_from_position((self.x+1, self.y))
                victim = ep_square.occupying_piece
                if self.is_victim_valid(victim):
                    available_squares.append(square)
                    self.en_passant = True
                        
            if self.x - 1 >= 0 and self.y == 4:
                square = board.get_square_from_position((self.x-1, self.y+1))
                ep_square = board.get_square_from_position((self.x-1, self.y))
                victim = ep_square.occupying_piece
                if victim and victim.notation == ' ':
                    if victim.boosted and not victim.stale:
                        available_squares.append(square)
                        self.en_passant = True

        return available_squares
    
    def attacking_squares(self, board):
        moves = []
        if self.colour == 'white':
            if self.x + 1 <= 7 and self.y - 1 >= 0:
                moves.append(board.get_square_from_position((self.x+1, self.y-1)))
            if self.x - 1 >= 0 and self.y - 1 >= 0:
                moves.append(board.get_square_from_position((self.x-1, self.y-1)))
        elif self.colour == 'black':
            if self.x + 1 <= 7 and self.y + 1 <= 7:
                moves.append(board.get_square_from_position((self.x+1, self.y+1)))
            if self.x - 1 >= 0 and self.y + 1 <= 7:
                moves.append(board.get_square_from_position((self.x-1, self.y+1)))
        return moves