import time

class Timer:
    #Initial time is the starting time in seconds for each game: E.g. 600 for a 10 minute game
    def __init__(self, initial_time):
        #Starting time for white and black, with white having the first move
        self.white_time = initial_time
        self.black_time = initial_time
        self.initial_time = initial_time
        self.start_time = None
        self.turn = 'white'

    #Starts the timer for each player, giving the amount of time start of the match
    def start(self):
        self.start_time = time.time()
    
    #Handles the pausing and resuming of the timer when the turn switches
    def switch_turn(self):
        #Calculates the amount of time used by a player
        elapsed = time.time() - self.start_time
        #Switches the turn and subtracts the amount of time used
        if self.turn == 'white':
            self.white_time -= elapsed
            self.turn = 'black'
        else:
            self.black_time -= elapsed
            self.turn = 'white'
        #Reset the timer for the next turn
        self.start_time = time.time()  

    def get_time(self, colour):
        elapsed = time.time() - self.start_time
        
        #Takes away from the timer
        if self.turn == 'white':
            self.white_time = max(0, self.white_time - elapsed)
        else:
            self.black_time = max(0, self.black_time - elapsed)
            
        #Resets to the initial time to avoid double subtraction
        self.start_time = time.time()
        
        #Returns whose turn it is
        if colour == 'white':
            return self.white_time
        return self.black_time



    #Checks if either player has run out of time
    def timeout(self):
        if self.white_time <= 0:
            return 'White'
        elif self.black_time <= 0:
            return 'Black'
        return None
