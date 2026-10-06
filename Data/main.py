# Importing the library and classes
import pygame
from Data.Classes.board import Board
from Data.Classes.game_over import show_game_over

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
    winner = None
    while running:
        # Get the position of the mouse
        mx, my = pygame.mouse.get_pos()
        for event in pygame.event.get():
            # Quit the game if the user presses the close button
            if event.type == pygame.QUIT:
                print("THE GAME HAS ENDED")
                running = False
                break
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # If the left mouse button is clicked
                if event.button == 1:
                    board.click_detection(mx, my)

        if board.checkmate:
            # Board.turn is switched to the checkmated player's colour.
            winner = "Black" if board.turn == "white" else "White"
            running = False
        elif board.end:
            running = False
        
        # Draw the board
        draw(display)

        # The board draw updates the active clock; check it immediately after.
        if running:
            timed_out = board.timer.timeout()
            if timed_out:
                winner = "Black" if timed_out == "White" else "White"
                running = False

    if winner:
        show_game_over(display, winner, duration_ms=5000)
