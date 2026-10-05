# Importing the library and classes
import pygame
from Data.Classes.board import Board

def draw(display):
    display.fill('white')
    board.draw(display)
    pygame.display.update()

board = None

def chess():
    global board
    # Initializing Pygame
    pygame.init()
    board = Board(400, 400)

    # Creating the display
    display = pygame.display.set_mode((800, 600))
    pygame.display.set_caption('CHESS ULTIMA') 
    
    running = True
    while running:
        # Get the position of the mouse
        mx, my = pygame.mouse.get_pos()
        for event in pygame.event.get():
            # Quit the game if the user presses the close button
            if event.type == pygame.QUIT:
                print("THE GAME HAS ENDED")
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # If the left mouse button is clicked
                if event.button == 1:
                    board.click_detection(mx, my)

        if board.end:
            running = False
        
        # Draw the board
        draw(display)

if __name__ == "__main__":
    chess()
