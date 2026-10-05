import pygame
from Data.Classes.square import Square
from Data.Classes.pieces.bishop import Bishop
from Data.Classes.pieces.king import King
from Data.Classes.pieces.knight import Knight
from Data.Classes.pieces.pawn import Pawn
from Data.Classes.pieces.queen import Queen
from Data.Classes.pieces.rook import Rook
from Data.Classes.timer import Timer
import random
import time

class Board:
    def __init__ (self, width, height):
        self.width = width
        self.height = height
        self.square_width = width // 8
        self.square_height = height // 8
        self.selected = None
        self.turn = 'white'
        self.board_design = [
            ['bR', 'bN', 'bB', 'bQ', 'bK', 'bB', 'bN', 'bR'],#8th Rank
            ['bP', 'bP', 'bP', 'bP', 'bP', 'bP', 'bP', 'bP'],#7th Rank
            ['', '', '', '', '', '', '', ''],                #6th Rank
            ['', '', '', '', '', '', '', ''],                #5th Rank
            ['', '', '', '', '', '', '', ''],                #4th Rank
            ['', '', '', '', '', '', '', ''],                #3rd Rank
            ['wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP'],#2nd Rank
            ['wR', 'wN', 'wB', 'wQ', 'wK', 'wB', 'wN', 'wR'] #1st Rank
                ]
        self.squares = self.generate_squares()
        self.setup_board()
        self.wcheck = False
        self.bcheck = False
        self.check = False
        self.checking_pieces = []
        self.checking_direction = []
        self.checkmate = False
        self.stalemate = False
        self.check_cache = {}
        #Initial position of the board for threefold repetition
        self.initial_position = []
        for square in self.squares:
            if square.occupying_piece:
                self.initial_position.append(square.occupying_piece.colour+square.occupying_piece.notation)
            else:
                self.initial_position.append(None)
        self.timer = Timer(600)
        self.timer.start()
        self.prev_positions = [self.initial_position]
        self.position_counter = [1]
        self.white_pieces = []
        self.black_pieces = []
        self.my_pieces = []
        self.opp_pieces = []
        self.end = False
        self.die = False
        self.xdie = False

    def generate_squares(self): 
        square_list = []
        for y in range(0, 8):
            for x in range(0, 8):
                square_list.append(Square(x,  y, self.square_width, self.square_height))
        return square_list
    
    def get_square_from_position(self, position):
        for square in self.squares:
            if (square.x, square.y) == (position[0], position[1]):
                return square
            elif (square.position_x, square.position_y) == (position[0], position[1]):
                return square

    def get_piece_from_position(self, position):
        #Returns the position of the piece
        if self.get_square_from_position(position):
            return self.get_square_from_position(position).occupying_piece
    
    def setup_board(self):
        print('Setting up the board')
        for y, row in enumerate(self.board_design):
            for x, piece in enumerate(row):
                if piece:
                    square = self.get_square_from_position((x, y))
                    colour = 'white' if piece[0] == 'w' else 'black'
                    piece_class = {
                        'B': Bishop,
                        'K': King,
                        'N': Knight,
                        'P': Pawn,
                        'Q': Queen,
                        'R': Rook
                    }.get(piece[1])
                    if square != None:
                        square.occupying_piece = piece_class((x, y), colour, self)
                    else:
                        continue
    
    def click_detection(self, mx, my):
        x = mx // self.square_width
        y = my // self.square_height
        clicked_square = self.get_square_from_position((x, y))
        available_moves = False
        
        if self.selected == None:
            if clicked_square and clicked_square.occupying_piece:
                if clicked_square.occupying_piece.colour == self.turn:
                    self.selected = clicked_square.occupying_piece
        
        #Otherwise, if a move is made...   
        elif self.selected.move(self, clicked_square):
            material = []
            pair = []
            board_design = []
            self.timer.switch_turn()
            self.end = False
        
            #THREEFOLD REPETITION
            #Creates a list of the pieces on every square
            for square in self.squares:
                if square.occupying_piece:
                    board_design.append(square.occupying_piece.colour + square.occupying_piece.notation)
                else:
                    board_design.append(None)
            #If the position hasn't occurred already...
            if board_design not in self.prev_positions:
                #Add it to the list of previously occured positions and add a counter to another list in the same index
                self.prev_positions.append(board_design)
                self.position_counter.append(1)
            #Otherwise...
            else:
                #Add 1 to the counter of that list
                index = self.prev_positions.index(board_design)
                self.position_counter[index] += 1

            for i in range(0, len(self.position_counter) - 1):
                if self.position_counter[i] == 3:
                    print('Draw by threefold repetition')
                    self.end = True
                    break
            
            #INSUFFICIENT MATERIAL
            #Gets the material of the game after each move
            for square in self.squares:
                if square.occupying_piece:
                    #Adds the piece colour and type to the material
                    material.append(square.occupying_piece.colour + square.occupying_piece.notation)
                #The most amount of material that can be considered 'insufficient' is 4. If there are 5 or more pieces on the board, the is indeed sufficient material
                if len(material) > 4:
                    break
            #Due to the rules of the game, the two kings can never be removed, meaning there will always be at least 2 pieces on the board
            #King vs King 
            if len(material) == 2:
                print('Draw by insufficient material')
                self.end = True
            elif len (material) == 3:
                #King & Knight vs King
                if 'whiteN' in material or 'blackN' in material:
                    print('Draw by insufficient material')
                    self.end = True
                #King & Bishop vs King
                elif 'whiteB' in material or 'blackB' in material:
                    print('Draw by insufficient material')
                    self.end = True
            elif len(material) == 4:
                #King & Knight vs King & Knight
                if 'whiteN' in material and 'blackN' in material:
                    print('Draw by insufficient material')
                    self.end = True
                #King & Bishop vs King & Bishop
                elif 'whiteB' in material and 'blackB' in material:
                    #Makes sure they are ofm different colour squares
                    for square in self.squares:
                        if square.occupying_piece and square.occupying_piece.notation == 'B':
                            pair.append(square.colour)
                    if pair[0] != pair[1]:
                        print('Draw by insufficient material')
                        self.end = True
                            
            #CHECKMATE / STALEMATE
            #Checks if the player has legal moves
            for square in self.squares:
                if square.occupying_piece and square.occupying_piece.colour != self.turn:
                    if square.occupying_piece.valid_moves(self) != []:
                        available_moves = True
                        break
                        
            #Sets the conditions for checkmate and stalemate            
            if available_moves == False:
                if self.is_in_check() == True:
                    self.checkmate = True
                else:
                    self.stalemate = True
                self.end = True
                           
            #Switches the turn
            if self.turn == 'white':
                self.turn = 'black'
            elif self.turn == 'black':
                self.turn = 'white'
            self.selected = None
                        
            #Prints whether the a player is in checkmate or stalemate
            if self.checkmate == True:
                print(self.turn + ' is in checkmate!')
            elif self.stalemate == True:
                print('The game is in a draw via stalemate!')
                
        elif clicked_square and clicked_square.occupying_piece and clicked_square.occupying_piece.colour == self.turn:
            self.selected = clicked_square.occupying_piece
            
        else:
            self.selected = None
    
    def my_king(self):
        for square in self.squares:
            piece = square.occupying_piece
            if piece and piece.notation == 'K' and piece.colour == self.turn:
                return piece
            
    def opp_king(self):
        for square in self.squares:
            piece = square.occupying_piece
            if piece and piece.notation == 'K' and piece.colour != self.turn:
                return piece
            
    def get_pieces(self, board):
        pieces = []
        for square in board.squares:
            if square.occupying_piece:
                #Sorts pieces based on colour
                if square.occupying_piece.colour == 'white':
                    self.white_pieces.append(square.occupying_piece)
                else:
                    self.black_pieces.append(square.occupying_piece)
                #Determines if they are on the player's side
                if square.occupying_piece.colour == self.my_king():
                    self.my_pieces.append(square.occupying_piece)
                else:
                    self.opp_pieces.append(square.occupying_piece)
                
    def is_in_check(self):
        king = self.opp_king()
        if king is None:
            self.checking_pieces = []
            self.checking_direction = []
            return False

        king_square = self.get_square_from_position(king.position)
        checking_pieces = []
        checking_directions = []

        for square in self.squares:
            piece = square.occupying_piece
            if piece is None or piece.colour != self.turn:
                continue

            # Pawns move forward but attack diagonally.
            if piece.notation == ' ':
                if king_square in piece.attacking_squares(self):
                    checking_pieces.append(piece)
                    checking_directions.append([square, king_square])
                continue

            if king_square not in piece.get_moves(self):
                continue

            checking_pieces.append(piece)
            for direction in piece.get_possible_moves(self):
                if isinstance(direction, list) and king_square in direction:
                    # Keep the checker and the squares between it and the king
                    # so a reply can capture the checker or block the attack.
                    line = [square]
                    for line_square in direction:
                        line.append(line_square)
                        if line_square == king_square:
                            break
                    checking_directions.append(line)
                elif direction == king_square:
                    checking_directions.append([square, king_square])

        self.checking_pieces = checking_pieces
        self.checking_direction = checking_directions
        return bool(checking_pieces)
                    
    #Highlights squares.
    def draw(self, display):
        #Updates the highlighted squares when a piece is selected
        if self.selected != None:
            if self.get_square_from_position(self.selected.position):
                for square in self.squares:
                    square.highlight = False
                self.get_square_from_position(self.selected.position).highlight = True
                if self.selected.valid_moves(self):
                    for square in self.selected.valid_moves(self):
                        square.highlight = True
        for square in self.squares:
            square.draw(display)
    
        #Draws the timer
        font = pygame.font.Font(None, 36)
        white_time = self.timer.get_time('white')
        black_time = self.timer.get_time('black')
        #Converts time into minutes and seconds
        white_mins = int(white_time // 60)
        white_secs = int(white_time % 60)
        black_mins = int(black_time // 60)
        black_secs = int(black_time % 60)
        
        #Renders the text and places a 0 in front of any single digit values
        white_timer_text = font.render(f'White: {white_mins:02}:{white_secs:02}', True, (255, 255, 255))
        black_timer_text = font.render(f'Black: {black_mins:02}:{black_secs:02}', True, (0, 0, 0))

        #Positions the timer next to the board        
        #White Timer Box
        pygame.draw.rect(display, (50, 50, 50), pygame.Rect(self.width, self.height-38, 150, 38))
        display.blit(white_timer_text, (self.width+1, self.height-38))
        #Black Timer Box
        pygame.draw.rect(display, (200, 200, 200), pygame.Rect(self.width, 0, 150, 38))
        display.blit(black_timer_text, (self.width+1, 0))
                
    def material_timeout(self):
        if self.timer.timeout() == None:
            return False
        else:
            #If white runs out of time, checks if black has sufficient material
            if self.timer.timeout() == 'White':
                #Checks if there is only one piece left (just the king)
                if len(self.black_pieces) == 1:
                    return True
                #Only other combinations of insufficient material is king & bishop or king & knight
                elif len(self.black_pieces) == 2:
                    for piece in self.black_pieces:
                        if piece.notation == 'B' or piece.notation == 'N':
                            return True
                else:
                    return None
            #Repeats for black
            elif self.timer.timeout() == 'Black':
                if len(self.white_pieces) == 1:
                    return True
                elif len(self.white_pieces) == 2:
                    for piece in self.white_pieces:
                        if piece.notation == 'B' or piece.notation == 'N':
                            return True
                else:
                    return None
