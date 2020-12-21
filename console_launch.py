import time
from game_of_life import Life, display_life, display_scroll_text


def gol():
    iterations = 0
    while True: # process runs until manually killed
        # the update_life method creates a new life sequence and returns repeating if sequence is repeating.
        # if we have a repeating sequence, quit current game, and start new game while process_run is true
        game = Life(17, 7) # create a new game with the size of the LED screen
        # print('new game created')
        while game.update_life() == 'unique': # keeps looping as long as no repeating patterns
            # print_grid(game.life)
            display_life(game.life) # send the current game to display on the LED screen
            time.sleep(.5) # leave the display for a split second before refreshing
        # display the stats for each game before starting a new game.
        if game.update_life() == 'repeating': # end of game, patterns are now repeating
            display_scroll_text('Current game iteration was {}'.format(game.iteration), 5)
            if game.iteration > iterations:
                iterations = game.iteration

            display_scroll_text('Highest game iterations were {}'.format(iterations), 5)
        time.sleep(1)


gol()  # run the game
