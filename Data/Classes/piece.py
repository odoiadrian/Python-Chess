import pygame
#Used for the dice function and animation
import random
import time

class Piece:
    def __init__ (self, position, colour, board):
        self.position = position
        self.x = position[0]
        self.y = position[1]
        self.colour = colour
        self.has_moved = False
        self.stale = True
        self.checking_direction = None
        self.valid_moves_cache = {}
        
    #Collects all the availiable moves for each piece
    def get_moves (self, board):
        moves = []
        
        #Loops through all the possible moves
        for direction in self.get_possible_moves(board):
            if direction:
                #Used for pieces that aren't knights or pawns: Moves in the form of a 2D array
                if type(direction) == list:
                    for square in direction:
                        if square:
                            #If there is a piece occupying the square, the iteration plays
                            if square.occupying_piece:
                                #If the piece in the way is of the same colour, this loop stops and the square isn't added
                                if square.occupying_piece.colour == self.colour:
                                    break
                                else:
                                    moves.append(square)
                                    break
                            else:      
                                moves.append(square)
                            
                #Used purely for the knight and pawn: Moves in the form of a 1D array        
                elif type(direction) == object:
                    if direction.occupying_piece:
                        if direction.occupying_piece.colour != self.colour:
                            moves.append(direction)
                    else:
                        moves.append(direction)
        
        #Add pawn attacking squares
        if self.notation == ' ':
            for move in self.attacking_squares(board):
                if move.occupying_piece and move.occupying_piece.colour != self.colour:
                    moves.append(move)
                    
        return moves
    
    def _valid_moves(self, board):
        key = (self.x, self.y, self.colour)
        if key in self.valid_moves_cache:
            return self.valid_moves_cache[key]
        #Calculate the valid moves and store the result in the cache
        result = self.valid_moves(board)
        self.valid_moves_cache[key] = result
        return result

    def valid_moves(self, board):
        moves = []
        if self.notation == ' ':
            for move in self.attacking_squares(board):
                if move.occupying_piece and move.occupying_piece.colour != self.colour:
                    moves.append(move)

        #Get all possible moves for this piece
        for move in self.get_moves(board):
            moves.append(move)
        
        #Checks to see if any king is in check
        if board.bcheck or board.wcheck:
            #Prevents pieces from moving in a way that would leave the king in check
            if self.notation != 'K':
                for direction in board.checking_direction:
                    #Only applies to Queens, Bishops and Rooks
                    if type(direction) == list:
                        for move in moves:
                            if move not in direction:
                                moves.remove(move)

        #Prevent king from moving into check
        if self.notation == 'K':
            for square in board.squares:
                if square.occupying_piece and square.occupying_piece.colour != self.colour:
                    piece = square.occupying_piece
                    for squar in piece.get_moves(board):
                        if squar in self.get_moves(board) and squar in moves:
                            moves.remove(squar)
        #Prevents pinned pieces from exposing the king
        if self.notation != 'K':
            for square in board.squares:
                if square.occupying_piece and square.occupying_piece.colour != self.colour:
                    attacker = square.occupying_piece
                    #Checks if attacker is a queen, rook, or bishop
                    if attacker.notation in ['Q', 'R', 'B']:
                        #Gets the direction
                        for direction in attacker.get_possible_moves(board):
                            if type(direction) == list:
                                piece_in_line = False
                                king_in_line = False
                                #Check each individual move in said direction
                                for move in direction:
                                    if move:
                                        #Check if the current piece is in line
                                        if move.occupying_piece == self:
                                            piece_in_line = True
                                            #Check if the king is in line
                                        elif piece_in_line and move.occupying_piece == board.my_king():
                                            king_in_line = True
                                            break
                                        #Stop checking if another piece blocks the line
                                        elif move.occupying_piece:
                                            break

                                    #If pinned, only allow them to go in line with the pin direction
                                    if piece_in_line and king_in_line:
                                        moves = []
                                        if move in direction:
                                            moves.append(move)


        #Prevent the king from moving into attack by pawns
        if self.notation == 'K':
            for move in moves:
                    if move in self.cant_go(board):
                        moves.remove(move)

        #Prevent castling if attacked
        if self.notation == 'K':
            if board.get_square_from_position((self.x + 1, self.y)) not in moves and board.get_square_from_position((self.x + 2, self.y)) in moves:
                    moves.remove(board.get_square_from_position((self.x + 2, self.y)))
            if board.get_square_from_position((self.x - 1, self.y)) not in moves and board.get_square_from_position((self.x - 2, self.y)) in moves:
                    moves.remove(board.get_square_from_position((self.x - 2, self.y)))

        return moves


    def move (self, board, square, force = False):
        
        #The square variable is the desired square that the player wants the piece to move to
        for i in board.squares:
            i.highlight = False

        if self.position and (square in self.valid_moves(board) or force): #If the move is legal...
            #The previous square is now the square the piece was previously on
            prev_square = board.get_square_from_position(self.position)
            #The new position is now the desired square
            self.position = square.position
            self.x = square.x
            self.y = square.y
            
            #Tells if a pawn has boosted or not
            if self.notation == ' ':
                if self.y - prev_square.y == 2 or self.y - prev_square.y == -2:
                    self.boosted = True
                else:
                    self.boosted = False
            
            #Removes the enemy piece during En Passant
            if self.notation == ' ':
                if self.en_passant == True:
                    if self.colour == 'white':
                        passing_square = board.get_square_from_position((self.x, self.y - 1))
                    elif self.colour == 'black':
                        passing_square = board.get_square_from_position((self.x, self.y + 1))
                    if passing_square:
                        passing_square.occupying_piece = None
            
            #The previous square no longer has a piece on it
            if prev_square:
                prev_square.occupying_piece = None
            #The piece occupying the new square is the piece that was just moved
            square.occupying_piece = self
            #There are no longer any selected pieces
            board.selected = None
            #The piece has moved
            self.has_moved = True
            self.stale = False
            
            #Sets whether the piece is 'stale' or not
            for square in board.squares:
                if square and square.occupying_piece:
                    if square.occupying_piece != self:
                        square.occupying_piece.stale = True
                    else:
                        square.occupying_piece.stale = False
                        
            #Promoting Pawns (Only allows the Queen for now for simplicity)
            if self.notation == ' ':
                if (self.y == 0) or (self.y == 7):
                    from Data. Classes. pieces. queen import Queen
                    square.occupying_piece = Queen((self.x, self.y), self.colour, board)                    
            
            #Castling
            if self.notation == 'K':
                #Long Castling (O-O-O)
                if prev_square.x - self.x == 2:
                    rook = board.get_piece_from_position((0, self.y))
                    rook.move(board, board.get_square_from_position((3, self.y)), force=True)
                #Short Castling (O-O)
                elif prev_square.x - self.x == -2:
                    rook = board.get_piece_from_position((7, self.y))
                    rook.move(board, board.get_square_from_position((5, self.y)), force=True)
            else:
                board.selected = None
            
            
            #Determines who is in check
            if board.is_in_check() == True:
                if board.turn == 'black':
                    board.wcheck = True
                    board.bcheck = False
                else:
                    board.wcheck = False
                    board.bcheck = True
            else:
                board.wcheck = False
                board.bcheck = False
                
            return True      
            
        else: #If the move is illegal...
            board.selected = None
            return False
    
