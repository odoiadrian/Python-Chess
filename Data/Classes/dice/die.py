import pygame
import random
import time

pygame.init()

class Die:
    def __init__ (self, position, dimensions):
        x, y = position
        self.width, self.height = dimensions        
        self.font = pygame.font.Font(None, 100)
        self.fps = 10


        #Dice rolling animation
        def roll_dice(self):
            for _ in range(10): 
                num = random.randint(1, 7)
                #Renders the font and colour of the number
                text = FONT.render(str(num), True, (0, 0, 0))
                screen.blit(text, (self.width//2 - 30, self.height//2 - 50))
                pygame.display.flip()
            return num

        #Main loop
        running = True
        dice_value = 1  # Initial dice value
        while running:
            screen.fill(WHITE)
            
            # Display dice value
            text = FONT.render(str(dice_value), True, BLACK)
            screen.blit(text, (WIDTH//2 - 30, HEIGHT//2 - 50))
            
            pygame.display.flip()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:  # Roll on spacebar press
                        dice_value = roll_dice()

        pygame.quit()
    `