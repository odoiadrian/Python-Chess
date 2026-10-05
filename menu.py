import pygame
import sys

#Start Pygame
pygame.init()

#Set up the screen
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Main Menu")

#Colours
background_colour = (0, 0, 0)
text_colour = (255, 255, 255)
hover_box_colour = (100, 100, 100)

#Font
font = pygame.font.Font(None, 50)

#Menu options
menu_options = ["Start Game", "Quit"]

#Draw the menu
def draw_menu():
    #Fill the screen with the background colour
    screen.fill(background_colour)

    #Get the position of the mouse
    mouse_x, mouse_y = pygame.mouse.get_pos()

    #Draw each menu option
    for i, option in enumerate(menu_options):
        text = font.render(option, True, text_colour)
        text_rect = text.get_rect(center=(screen_width // 2, 200 + i * 100))

        #If the mouse is hovering over the option...
        if text_rect.collidepoint(mouse_x, mouse_y):
            #Draw a grey box around the option
            pygame.draw.rect(screen, hover_box_colour, text_rect.inflate(20, 20))
        
        #Draw the option text
        screen.blit(text, text_rect)

#Main menu
def main_menu():
    while True:
        #Check for interactions with the interface like clicking
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                for i, option in enumerate(menu_options):
                    text_rect = font.render(option, True, text_colour).get_rect(center=(screen_width // 2, i * 100 + 200))
                    
                    if text_rect.collidepoint(mouse_x, mouse_y):
                        #Starts there game if the user clicked "Start Game"
                        if option == "Start Game":
                            from main import chess
                            chess()
                            pygame.display.set_caption("Main Menu")
                        #Quits the game if the user clicked "Quit"
                        elif option == "Quit":
                            pygame.quit()
                            sys.exit()

        #Draws the menu
        draw_menu()

        #Update the display
        pygame.display.flip()

#Run the main menu
main_menu()
