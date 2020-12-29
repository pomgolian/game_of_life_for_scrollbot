import time
from game_of_life import Life, display_life, display_scroll_text
import scrollphathd as sphd
from astral import LocationInfo
from astral.sun import sun
import datetime


loc = LocationInfo(name='Melbourne', region='Australia', timezone='Australia/Melbourne',
                   latitude=-37.840935, longitude=144.946457)
s = sun(loc.observer, date=datetime.date.today(), tzinfo=loc.timezone)


sphd.rotate(180)  # flip the screen for a scrollbot


def gol():
    iterations = 0
    while True: # process runs until manually killed
        # the update_life method creates a new life sequence and returns repeating if sequence is repeating.
        # if we have a repeating sequence, quit current game, and start new game
        game = Life(17, 7) # create a new game with the size of the LED screen
        # print('new game created')
        # see if it is dark outside to set the default brightness
        if s['sunrise'].replace(tzinfo=None) < datetime.datetime.now() < s['sunset'].replace(tzinfo=None):
            # print('daytime')
            sphd.set_brightness(0.25)  # set a default brightness at 25%
        else:
            # print('nighttime')
            sphd.set_brightness(0.1)  # set a default brightness at 10%
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
