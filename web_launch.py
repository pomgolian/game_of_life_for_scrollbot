from flask import Flask, render_template, url_for, request
from threading import Thread
import time
from game_of_life import Life, display_life

from werkzeug.utils import redirect

process_run = False

app = Flask(__name__)


def spawn_async_process(process_name):
    if process_name == 'game_of_life':
        Thread(target=gol, args=()).start()


def gol():
    global process_run
    iterations = 0
    while process_run: # process_run gets set to True from web page submit
        # the update_life method creates a new life sequence and returns repeating if sequence is repeating.
        # if we have a repeating sequence, quit current game, and start new game while process_run is true
        game = Life(17, 7) # create a new game with the size of the LED screen
        # print('new game created')
        while game.update_life() == 'unique' and process_run: # keeps looping as long as no repeating patterns
            # print_grid(game.life)
            display_life(game.life) # send the current game to display on the LED screen
            time.sleep(.5) # leave the display for a split second before refreshing
        # todo display the stats for each game before starting a new game.
        if game.update_life() == 'repeating': # end of game, patterns are now repeating
            print('Current game iteration was {}'.format(game.iteration))
            if game.iteration > iterations:
                iterations = game.iteration
            print('Highest game iterations were {}'.format(iterations))
            print('------')
        time.sleep(2)


@app.route('/')
def front_page():
    my_process = 'game_of_life'
    spawn_async_process(my_process)
    return render_template("web_run.html")


@app.route('/stop')
def stop():
    global process_run
    process_run = False
    return redirect(url_for('front_page'))


@app.route('/start')
def start():
    global process_run
    process_run = True
    return redirect(url_for('front_page'))


if __name__ == '__main__':
    app.run()
