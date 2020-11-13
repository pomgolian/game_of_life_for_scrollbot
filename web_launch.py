from flask import Flask, render_template, url_for, request
from threading import Thread
import time
from game_of_life import Life, display_life

from werkzeug.utils import redirect

app = Flask(__name__)

if 'process_status' not in globals():
    process_status = 'stopped'


if 'process_spawned' not in globals():
    process_spawned = False


def spawn_async_process(process_name):
    if process_name == 'game_of_life':
        Thread(target=gol, args=()).start()


def gol():
    global process_status
    global process_spawned
    process_spawned = True
    iterations = 0
    while process_status == 'running': # process_run gets set to running from web page submit
        # the update_life method creates a new life sequence and returns repeating if sequence is repeating.
        # if we have a repeating sequence, quit current game, and start new game while process_run is true
        game = Life(17, 7) # create a new game with the size of the LED screen
        # print('new game created')
        while game.update_life() == 'unique' and process_status == 'running': # keeps looping as long as no repeating patterns
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
    process_spawned = False


@app.route('/')
def front_page():
    global process_status
    global process_spawned
    my_process = 'game_of_life'
    print('process is {}'.format(process_spawned))
    if process_spawned is False and process_status == 'running':
        print('spawned a process')
        spawn_async_process(my_process)
    else:
        print('did not spawn')
    return render_template("web_run.html", process_status=process_status)


@app.route('/stop')
def stop():
    global process_status
    process_status = 'stopped'
    return redirect(url_for('front_page'))


@app.route('/start')
def start():
    global process_status
    process_status = 'running'
    return redirect(url_for('front_page'))


if __name__ == '__main__':
    app.run(host='127.0.0.1')
