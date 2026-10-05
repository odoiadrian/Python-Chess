import pygame

class Square:
    def __init__ (self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.position_x = x * width
        self.position_y = y * height
        self.position = (self.position_x, self.position_y)
        self.positional = (x, y)
        self.had = False
        
        #Determines if the square is highlighted and if there is a piece there
        self.highlight = False
        self.occupying_piece = None
        
        #Determines the colour of the square
        if (x+y) % 2 == 1:
            self.colour = 'dark'
            self.default_colour = (50, 50, 50)
            self.highlight_colour = (0, 77, 0)
        else:
            self.colour = 'light'
            self.default_colour = (255, 255, 255)
            self.highlight_colour = (50, 255, 50)
        
        self.notation = self.get_notation()
        self.rect = pygame.Rect (self.position_x, self.position_y, self.width, self.height)
        
    def get_notation (self):
        files = 'abcdefgh'
        return files[self.x] + str(8 - self.y)
        
    def draw (self, display):
        #Draws the square colour
        if self.highlight == True:
            pygame.draw.rect(display, self.highlight_colour, self.rect)
        else:
            pygame.draw.rect(display, self.default_colour, self.rect)
            
        #Draws the piece if there is one on the square
        if self.occupying_piece != None:
            image = self.occupying_piece.img
            centering_rect = image.get_rect()
            centering_rect.center = self.rect.center
            display.blit(self.occupying_piece.img, centering_rect.topleft)