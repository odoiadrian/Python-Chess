#Board.py
#line 286
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


    import time
    def dice_roll(self, display, font, x, y):
        if not self.die:
            return None

        #Define the range of numbers for the 7-sided die
        numbers = list(range(1, 8))

        #Simulate the dice rolling animation
        for _ in range(10):  #Number of frames for animation
            rolled_number = random.choice(numbers)

            #Clear previous dice roll area
            pygame.draw.rect(display, (0, 0, 0), (x, y, 50, 50))

            #Render and display the rolling number
            dice_text = font.render(str(rolled_number), True, (255, 255, 255))
            display.blit(dice_text, (x + 10, y + 10))

            pygame.display.update()
            time.sleep(0.1)  #Small delay for animation effect

        #Result of the roll
        result = random.choice(numbers)

        #Clear the rolling effect to display the final result
        pygame.draw.rect(display, (0, 0, 0), (x, y, 50, 50))
        dice_text = font.render(str(result), True, (255, 255, 255))
        display.blit(dice_text, (x + 10, y + 10))
        pygame.display.update()

        return result



